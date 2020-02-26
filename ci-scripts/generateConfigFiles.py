#/*
# * Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
# * contributor license agreements.  See the NOTICE file distributed with
# * this work for additional information regarding copyright ownership.
# * The OpenAirInterface Software Alliance licenses this file to You under
# * the OAI Public License, Version 1.1  (the "License"); you may not use this file
# * except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *      http://www.openairinterface.org/?page_id=698
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *-------------------------------------------------------------------------------
# * For more information about the OpenAirInterface (OAI) Software Alliance:
# *      contact@openairinterface.org
# */
#---------------------------------------------------------------------

import os
import re
import sys

def GenerateHssConfigurer(cassandra_IP, hss_s6a_IP):
	hssFile = open('./hss-cfg.sh', 'w')
	hssFile.write('#!/bin/bash\n')
	hssFile.write('\n')
	hssFile.write('cd /home/scripts\n')
	hssFile.write('\n')
	# CASSANDRA ADDRESS SHOULD BE THE CASSANDRA CONTAINER default address
	hssFile.write('Cassandra_Server_IP=\'' + cassandra_IP + '\'\n')
	hssFile.write('PREFIX=\'/usr/local/etc/oai\'\n')
	# The following variables could be later be passed as parameters
	hssFile.write('MY_REALM=\'openairinterface.org\'\n')
	hssFile.write('MY_APN=\'apn.oai.svc.cluster.local\'\n')
	hssFile.write('MY_LTE_K=\'8baf473f2f8fd09487cccbd7097c6862\'\n')
	hssFile.write('MY_OP_K=\'11111111111111111111111111111111\'\n')
	hssFile.write('\n')
	hssFile.write('rm -Rf $PREFIX\n')
	hssFile.write('\n')
	hssFile.write('mkdir -p $PREFIX\n')
	hssFile.write('mkdir $PREFIX/freeDiameter\n')
	hssFile.write('mkdir $PREFIX/logs\n')
	hssFile.write('\n')
	hssFile.write('# provision users\n')
	hssFile.write('./data_provisioning_users --apn $MY_APN --apn2 internet --key $MY_LTE_K --imsi-first 311480100001101 --msisdn-first 00000001 --mme-identity mme.$MY_REALM --no-of-users 10 --realm $MY_REALM --truncate True --verbose True --cassandra-cluster $Cassandra_Server_IP\n')
	hssFile.write('# provision mme\n')
	hssFile.write('./data_provisioning_mme --id 3 --mme-identity mme.$MY_REALM --realm $MY_REALM --ue-reachability 1 --truncate True  --verbose True -C $Cassandra_Server_IP\n')
	hssFile.write('\n')
	hssFile.write('cp ../etc/acl.conf ../etc/hss_rel14_fd.conf $PREFIX/freeDiameter\n')
	hssFile.write('cp ../etc/hss_rel14.conf ../etc/hss_rel14.json $PREFIX\n')
	hssFile.write('cp ../etc/oss.json $PREFIX\n')
	hssFile.write('\n')
	hssFile.write('declare -A HSS_CONF\n')
	hssFile.write('HSS_CONF[@PREFIX@]=$PREFIX\n')
	hssFile.write('HSS_CONF[@REALM@]=$MY_REALM\n')
	hssFile.write('HSS_CONF[@HSS_FQDN@]="hss.${HSS_CONF[@REALM@]}"\n')
	hssFile.write('HSS_CONF[@cassandra_Server_IP@]=$Cassandra_Server_IP\n')
	hssFile.write('HSS_CONF[@OP_KEY@]=$MY_OP_K\n')
	hssFile.write('HSS_CONF[@ROAMING_ALLOWED@]=\'true\'\n')
	hssFile.write('for K in "${!HSS_CONF[@]}"; do    egrep -lRZ "$K" $PREFIX | xargs -0 -l sed -i -e "s|$K|${HSS_CONF[$K]}|g"; done\n')
	# HSS S6A is for the moment the default OAI-HSS Container
	# We could later dedicate a container new interface
	hssFile.write('sed -i -e "s/#ListenOn.*$/ListenOn = "' + hss_s6a_IP + '";/g" $PREFIX/freeDiameter/hss_rel14_fd.conf\n')
	hssFile.write('../src/hss_rel14/bin/make_certs.sh hss ${HSS_CONF[@REALM@]} $PREFIX\n')
	hssFile.close()


#-----------------------------------------------------------
# Usage()
#-----------------------------------------------------------
def Usage():
	print('----------------------------------------------------------------------------------------------------------------------')
	print('generateConfigFiles.py')
	print('----------------------------------------------------------------------------------------------------------------------')
	print('Usage: python3 main.py [options]')
	print('  --help  Show this help.')
	print('---------------------------------------------------------------------------------------------------- HSS Options -----')
	print('  --kind=HSS')
	print('  --cassandra=[Cassandra IP server]')
	print('  --hss_s6a=[HSS S6A Interface IP server]')
	print('---------------------------------------------------------------------------------------------------- MME Options -----')
	print('  --kind=MME')
	print('  --hss_s6a=[HSS S6A Interface IP server]')
	print('  --mme_s6a=[MME S6A Interface IP server]')

argvs = sys.argv
argc = len(argvs)
cwd = os.getcwd()

kind = ''
cassandra_IP = ''
hss_s6a_IP = ''
mme_s6a_IP = ''

while len(argvs) > 1:
	myArgv = argvs.pop(1)
	if re.match('^\-\-help$', myArgv, re.IGNORECASE):
		Usage()
		sys.exit(0)
	elif re.match('^\-\-kind=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-kind=(.+)$', myArgv, re.IGNORECASE)
		kind = matchReg.group(1)
	elif re.match('^\-\-cassandra=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-cassandra=(.+)$', myArgv, re.IGNORECASE)
		cassandra_IP = matchReg.group(1)
	elif re.match('^\-\-hss_s6a=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-hss_s6a=(.+)$', myArgv, re.IGNORECASE)
		hss_s6a_IP = matchReg.group(1)
	elif re.match('^\-\-mme_s6a-(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-mme_s6a=(.+)$', myArgv, re.IGNORECASE)
		mme_s6a_IP = matchReg.group(1)
	else:
		Usage()
		sys.exit('Invalid Parameter: ' + myArgv)

if kind == '':
	Usage()
	sys.exit('missing kind parameter')

if kind == 'HSS':
	if cassandra_IP == '':
		Usage()
		sys.exit('missing Cassandra IP address')
	elif hss_s6a_IP == '':
		Usage()
		sys.exit('missing HSS S6A IP address')
	else:
		GenerateHssConfigurer(cassandra_IP, hss_s6a_IP)
		sys.exit(0)
