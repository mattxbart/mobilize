#!/bin/sh
ANSIBLE='/home/mbartolome/mobiletest/mobilize/ansible'
VIRTUAL_ENV='/home/mbartolome/mobiletest'

$VIRTUAL_ENV/bin/python $VIRTUAL_ENV/mobilize/run.py
$VIRTUAL_ENV/bin/ansible-playbook $ANSIBLE/playbook.yml -i $ANSIBLE/production

