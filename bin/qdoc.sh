#!/bin/bash

MODULE=""
HGBIN=/usr/local/bin/hg

while [ $# -gt 0 ] ; do
    case $1 in
      --recip)
  shift
  RECIP="$RECIP $1"
        shift
  ;;
      --module)
        shift
  MODULE=$1
        shift
  ;;
    esac
done

if [ -z $RECIP ]; then
        echo "No recipients to notify, use --recip ..."
        exit 0
fi

##############################################################################

# The version of your project to display within the documentation.
version=`$HGBIN id -n -r tip`

SUBJECT=$($HGBIN log -r tip --template '{desc|firstline}')

`dirname $0`/qdoc.py -v $version -f nginx@qbix.com -t $RECIP -s "$MODULE: $SUBJECT" &

echo "Started to generate API documentation"
exit 0