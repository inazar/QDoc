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
      --home)
        shift
    # The location of your qdoc install
  qdoc_home=$1
        shift
  ;;
      --base)
        shift
  base=$1
        shift
  ;;
    esac
done

if [ -z $qdoc_home ]; then
        echo "No home directory defined, use --home ..."
        exit 0
fi
if [ -z $base ]; then
        echo "No base directory defined, use --base ..."
        exit 0
fi
if [ -z $RECIP ]; then
        echo "No recipients to notify, use --recip ..."
        exit 0
fi

HGBIN=/usr/local/bin/hg

# The location of your yuidoc install
#qdoc_home=~/Projects/QDoc

# The location of the files to parse.  Parses subdirectories, but will fail if
# there are duplicate file names in these directories.  You can specify multiple
# source trees:
#     parser_in="%HOME/www/yui/src %HOME/www/event/src"
#parser_base="$HOME/Projects/QDoc/src"
parser_in="$base/src/Q $base/src/Db $base/src/plugins/Awards $base/src/plugins/Broadcast $base/src/plugins/Metrics $base/src/plugins/Places $base/src/plugins/Streams $base/src/plugins/Users"

# The location of the template files.  Any subdirectories here will be copied
# verbatim to the destination directory.
template=$qdoc_home/template

# The version of YUI the project is using.  This effects the output for
# YUI configuration attributes.  This should start with '2' or '3'.
yuiversion=2

# The location to output the parser data.  This output is a file containing a
# json string, and copies of the parsed files.
php_parser_out="$base/php/parser"

# The directory to put the html file outputted by the generator
php_generator_out="$base/php/web"

# The location to output the parser data.  This output is a file containing a
# json string, and copies of the parsed files.
node_parser_out="$base/node/parser"

# The directory to put the html file outputted by the generator
node_generator_out="$base/node/web"

##############################################################################

makeDocs()
{
  # The version of your project to display within the documentation.
  version=`$HGBIN id -n -r tip`

  SUBJECT=$($HGBIN log -r tip --template '{desc|firstline}')

  OUTPUT=$(
  $qdoc_home/bin/yuidoc.py $parser_in -p $php_parser_out -o $php_generator_out -t $template -v $version -Y $yuiversion -m "Q Framework (PHP)" -s -u "http://framework.qbix.com" -C "Qbix LLC." -e php  -x "Zend" -x "Facebook" 2>&1;
  $qdoc_home/bin/yuidoc.py $parser_in -p $node_parser_out -o $node_generator_out -t $template -v $version -Y $yuiversion -m "Q Framework (node.js)" -s -u "http://framework.qbix.com" -C "Qbix LLC." 2>&1
  )

  if [ -n "$OUTPUT" ]
  then
    echo "RECIP: $RECIP"
    echo "SUBJECT: '$MODULE: $SUBJECT'"
    echo "$OUTPUT"
  # echo $OUTPUT | mail -s "$MODULE: $SUBJECT" $RECIP
  fi
}

makeDocs &