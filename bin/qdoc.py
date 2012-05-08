#!/usr/bin/env python2.6

import yuidoc_parse, yuidoc_highlight, yuidoc_generate
import sys, os, logging, logging.config
from const import *

qddir, tmp = os.path.split(sys.path[0])
basedir, tmp = os.path.split(qddir)

frameworkList = ["Q", "Db", "plugins/Awards", "plugins/Broadcast", "plugins/Metrics", "plugins/Places", "plugins/Streams", "plugins/Users"]
clientList = []
parserIn = [
	(
		"PHP API",
		"/src/",
		frameworkList,
		".php",
		"php",
		["Zend", "Facebook"]
		),
	(
		"node.js API",
		"/src/",
		frameworkList,
		".js",
		"node",
		[]
		),
	(
		"client API",
		"/client/",
		clientList,
		".js",
		"node",
		[]
		)
	]

def main():
	from optparse import OptionParser
	optparser = OptionParser("usage: %prog [options]")
	optparser.set_defaults(extension=".js", 
	                       newext=".highlighted",
	                       parseroutdir="/tmp", 
	                       outputdir="docs", 
	                       parserfile="parsed.json", 
	                       showprivate=True,
	                       project="Q Framework",
	                       version="",
	                       copyrighttag="Qbix LLC.",
	                       projecturl="http://framework.qbix.com",
	                       yuiversion=False,
	                       ydn=False
	                       )
	optparser.add_option( "-v", "--version",
		action="store", dest="version", type="string",
		help="The version of the project" )
	optparser.add_option( "-f", "--from",
		action="store", dest="fromaddr", type="string", default='',
		help="The sender for messages" )
	optparser.add_option( "-t", "--to",
		action="append", dest="toaddr", default=[],
		help="Where to send the messages" )
	optparser.add_option( "-s", "--subject",
		action="store", dest="subject", type="string", default='QDoc log message',
		help="The subject for messages" )

	(opts, inputdirs) = optparser.parse_args()

	if not opts.fromaddr or not opts.toaddr:
		optparser.error("Incorrect number of arguments")

	logging.custom = {"mailhost": "localhost", "fromaddr": opts.fromaddr, "toaddr": opts.toaddr, "subject": opts.subject}

	for params in parserIn:
		(comment, source, inputList, extension, outdir, exdir) = params
		inputdirs = []
		for dirname in inputList:
			inputdirs.append(basedir+source+dirname)
		if len(inputdirs) > 0:
			docparser = yuidoc_parse.DocParser(
				inputdirs, 
				basedir+'/docs/'+outdir+'/parser', 
				"parsed.json", 
				extension,
				opts.version,
				False,
				exdir
				)

			highlighter = yuidoc_highlight.DocHighlighter(
				[basedir+'/docs/'+outdir+'/parser'], 
				basedir+'/docs/'+outdir+'/parser', 
				extension,
				opts.newext,
				exdir
				)

			gen = yuidoc_generate.DocGenerator(
				basedir+'/docs/'+outdir+'/parser', 
				"parsed.json", 
				basedir+'/docs/'+outdir+'/web',
				basedir+'/template',
				opts.newext,
				opts.showprivate,
				opts.project,
				opts.version,
				opts.projecturl,
				False,
				opts.copyrighttag
				)

			gen.process()

if __name__ == '__main__':
    main()
