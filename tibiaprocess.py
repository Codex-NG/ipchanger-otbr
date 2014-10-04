#!/usr/bin/env python3.3
import os
from ptrace.debugger.debugger import PtraceDebugger

class TibiaProcess:
	ips = (
		"login01.tibia.com",
		"login02.tibia.com",
		"login03.tibia.com",
		"login04.tibia.com",
		"login05.tibia.com",
		"tibia01.cipsoft.com",
		"tibia02.cipsoft.com",
		"tibia03.cipsoft.com",
		"tibia04.cipsoft.com",
		"tibia05.cipsoft.com",
		"test.tibia.com",
		"test.cipsoft.com",
		"tibia2.cipsoft.com",
		"tibia1.cipsoft.com",
		"server.tibia.com",
		"server2.tibia.com"
	)

	rsas = (
		"124710459426827943004376449897985582167801707960697037164044904862948569380850421396904597686953877022394604239428185498284169068581802277612081027966724336319448537811441719076484340922854929273517308661370727105382899118999403808045846444647284499123164879035103627004668521005328367415259939915284902061793",
		"132127743205872284062295099082293384952776326496165507967876361843343953435544496682053323833394351797728954155097012103928360786959821132214473291575712138800495033169914814069637740318278150290733684032524174782740134357629699062987023311132821016569775488792221429527047321331896351555606801473202394175817"
	)

	ot_rsa = "109120132967399429278860960508995541528237502902798129123468757937266291492576446330739696001110603907230888610072655818825358503429057592827629436413108566029093628212635953836686562675849720620786279431090218017681061521755056710823876476444260558147179707119674283982419152118103759076030616683978566631413"

	def __init__(self, pid):
		self.maps = []
		self.pid = pid
		self.current_ip = None
		self.tracer = PtraceDebugger()
		self.tracer.addProcess(pid, False)

	def attach(self):
		self.tracer[self.pid].attach()
		self.maps.extend(self.tracer[self.pid].readMappings()[0:4])

	def detach(self):
		self.tracer[self.pid].detach()
		self.maps = None

	def changeRsa(self):
		offset = 0

		for rsa in self.rsas:
			for res in self.maps[0].search(bytes(rsa, 'utf-8')):
				print('RSA found at: ', res)
				self.tracer[self.pid].writeBytes(res, bytes(self.ot_rsa, 'utf-8'))
				print(self.tracer[self.pid].readBytes(res, 180))

	def changeIp(self, newip):
		addr = []

		for ip in self.ips:
			for res in self.maps[3].search(bytes(ip, 'utf-8')):
				self.tracer[self.pid].writeBytes(res, bytes(newip, 'utf-8'))
				if len(ip) > len(newip):
					for offset in range(len(newip), len(ip)):
						self.tracer[self.pid].writeBytes(res + offset, bytes('\x00', 'utf-8'))

				print(self.tracer[self.pid].readBytes(res, 19))

		self.ips = [newip]