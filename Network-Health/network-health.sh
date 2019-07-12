#!/bin/bash
# Ping uses both exit codes 1 and 2. Exit code 2 cannot be used for docker health checks,
# therefore we use this script to catch error code 2
HEALTH_CHECK_HOST="google.com"
HOST=${HEALTH_CHECK_HOST}
LOG_FILE="log-network-health.log"

if [[ -z "$HOST" ]]
then
    echo "Host  not set! Set env 'HEATH_CHECK_HOST'. For now, using default google.com"
    HOST="google.com"
fi

TODAY=`date +%Y-%m-%d` # or whatever pattern you desire
TIME=`date +%T`

ping -c 1 $HOST
STATUS=$?
if [[ ${STATUS} -ne 0 ]]
then
    echo "Network is down"
    echo $TODAY $TIME ", 0" >> $LOG_FILE
    exit 1
fi

echo $TODAY $TIME ", 1" >> $LOG_FILE
#echo $TODAY $TIME "1"
echo "Network is up"
exit 0
