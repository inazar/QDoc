#!/usr/bin/env python2.6

import yuidoc_parse, yuidoc_highlight, yuidoc_generate
import sys, os, logging, logging.config
from const import *

basedir, tmp = os.path.split(sys.path[0])

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

logging.custom = {"mailhost": "localhost", "fromaddr": "nginx@qbix.com", "toaddr": "nazar@qbix.com", "subject": "Test message from QDoc"}
logging.config.fileConfig(os.path.join(sys.path[0], LOGCONFIG))

log = logging.getLogger('yuidoc.tmp')

log.info("It works!!!")

def main():
	from optparse import OptionParser
	optparser = OptionParser("usage: %prog inputdir [options] inputdir")
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

	(opts, inputdirs) = optparser.parse_args()

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

#if __name__ == '__main__':
#    main()
