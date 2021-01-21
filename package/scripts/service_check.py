#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
from __future__ import print_function

import subprocess
import sys

from resource_management.core.resources.system import Execute
from resource_management.libraries.script import Script


class ServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)

        doc = '{"name": "Ambari Smoke test"}'
        index = "ambari_smoke_test"

        print("Running Elastic search service check", file=sys.stdout)

        # Make sure the service is actually up.  We can live without everything allocated.
        # Need both the retry and ES timeout.  Can hit the URL before ES is ready at all and get no response, but can
        # also hit ES before things are green.
        host = "localhost:9200"
        Execute("curl -s -XGET 'http://%s/_cluster/health?wait_for_status=green&timeout=120s&pretty'" % host,
                logoutput=True,
                tries=6,
                try_sleep=20
                )

        # Put a document into a new index.

        Execute("curl -s -XPUT '%s/%s/_doc/1?pretty' -H 'Content-Type: application/json' -d '%s'" % (host, index, doc), logoutput=True)

        # Retrieve the document.  Use subprocess because we actually need the results here.
        cmd_retrieve = "curl -s -XGET '%s/%s/_doc/1'" % (host, index)
        proc = subprocess.Popen(cmd_retrieve, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (stdout, stderr) = proc.communicate()
        response_retrieve = stdout
        print("Retrieval response is: %s" % response_retrieve)
        expected_retrieve = '{"_index":"%s","_type":"_doc","_id":"1","_version":1,"_seq_no":0,"_primary_term":1,"found":true,"_source":{"name": "Ambari Smoke test"}}' \
            % (index)
        print("Expected is          : %s" % expected_retrieve)

        # Delete the index
        cmd_delete = "curl -s -XDELETE '%s/%s'" % (host, index)
        proc = subprocess.Popen(cmd_delete, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (stdout, stderr) = proc.communicate()
        response_delete = stdout
        print("Delete index response is: %s" % response_delete)
        expected_delete = '{"acknowledged":true}'
        print("Expected is             : %s" % expected_delete)

        if (expected_retrieve == response_retrieve) and (expected_delete == response_delete):
            print("Smoke test able to communicate with Elasticsearch")
        else:
            print("Elasticsearch service unable to retrieve document.")
            sys.exit(1)

        exit(0)


if __name__ == "__main__":
    ServiceCheck().execute()
