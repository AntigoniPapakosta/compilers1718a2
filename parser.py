
import plex


# ... συμπληρώστε τον κώδικά σας για τον συντακτικό αναλυτή - αναγνωριστή της γλώσσας ...

import plex

class ParseError(Exception):
	""" A user defined exception class, to describe parse errors. """
	pass

class MyParser:
	""" A class encapsulating all parsing functionality
	for a particular grammar. """
	
	def create_scanner(self,fp):
		""" Creates a plex scanner for a particular grammar 
		to operate on file object fp. """

		# define some pattern constructs
		notop = plex.Str("not")
		andop = plex.Str("and")
		orop = plex.Str("or")
		true = plex.NoCase(plex.Str("true","t","1")) 
		false = plex.NoCase(plex.Str("false","f","0"))
		equals = plex.Str("=")

		letter = plex.Range("AZaz")
		digit = plex.Range("09")

		variable = letter + plex.Rep(letter | digit)
		parenthesis = plex.Str("(",")")
		keyword = plex.Str("print")		
		space = plex.Any(" \t\n")

		# the scanner lexicon - constructor argument is a list of (pattern,action ) tuples
		lexicon = plex.Lexicon([
			(notop,'NOT'),
			(andop,'AND'),
			(orop,'OR'),
			(true,'TRUE'),
			(false,'FALSE'),
			(equals,'='),
			(parenthesis,plex.TEXT),
			(keyword,'PRINT'),
			(space,plex.IGNORE),
			(variable, 'VARIABLE')
			])
		
		# create and store the scanner object
		self.scanner = plex.Scanner(lexicon,fp)
		
		# get initial lookahead
		self.la,self.val = self.next_token()


	def next_token(self):
		""" Returns tuple (next_token,matched-text). """
		
		return self.scanner.read()		


	def position(self):
		""" Utility function that returns position in text in case of errors.
		Here it simply returns the scanner position. """
		
		return self.scanner.position()


	def match(self,token):
		""" Consumes (matches with current lookahead) an expected token.
		Raises ParseError if anything else is found. Acquires new lookahead. """ 
		
		if self.la==token:
			self.la,self.val = self.next_token()
		else:
			raise ParseError("found {} instead of {}".format(self.la,token))


	def parse(self,fp):
		""" Creates scanner for input file object fp and calls the parse logic code. """
		
		# create the plex scanner for fp
		self.create_scanner(fp)
		self.stmt_list()
		
		# call parsing logic
		# self.session()

	def stmt_list(self):
		if self.la=='VARIABLE' or self.la=='PRINT':
			self.stmt()
			self.stmt_list()
		elif self.la is None:
			return
		else:
			raise ParseError("in stmt_list: VARIABLE or PRINT expected")


	def stmt(self):
		if self.la=='VARIABLE':
			self.match('VARIABLE')
			self.match('=')
			self.expr()
		elif self.la=='PRINT':
			self.match('PRINT')
			self.expr()
		else:
			raise ParseError("in stmt: VARIABLE or = or PRINT expected")


	def expr(self):
		if self.la=='(' or self.la=='VARIABLE' or self.la=='TRUE' or self.la=='FALSE' or self.la=='NOT':
			self.term()
			self.term_tail()
		else:
			raise ParseError("in expr: ( or VARIABLE or TRUE or FALSE expected ")

	def term_tail(self):
		if self.la=='OR':
			self.orop()
			self.term()
			self.term_tail()
		elif self.la==')' or self.la=='VARIABLE' or self.la=='PRINT':
			return
		elif self.la is None:
			return	
		else:
			raise ParseError("in term_tail: AND expected")

	def term(self):
		if self.la=='(' or self.la=='VARIABLE' or self.la=='TRUE' or self.la=='FALSE':
			self.factor()
			self.factor_tail()
		else:
			raise ParseError("in term: ( or VARIABLE or BOOLEAN expected")

	def factor_tail(self):
		if self.la=='AND':
			self.andop()
			self.factor()
			self.factor_tail()
		elif self.la==')' or self.la=='OR' or self.la=='VARIABLE' or self.la=='PRINT':
			return
		elif self.la is None:
			return
		else:
			raise ParseError("in factor_tail: NOT expected")

	def factor(self):
		if self.la=='(' or self.la=='VARIABLE' or self.la=='TRUE' or self.la=='FALSE':
			self.notop()
			self.FnotOp()
		else:
			raise ParseError("in factor: ( or variable or boolean expected")
	def FnotOp(self):
		if self.la=='(':
			self.match('(')
			self.expr()
			self.match(')')
		elif self.la=='VARIABLE':
			self.match('VARIABLE')
		elif  self.la=='TRUE' or self.la=='FALSE':
			self.boolean()
		else:
			raise ParseError("in ftopdsajkfds: ( or VAR or BOOL telwwww)")	

	def boolean(self):
		if self.la=='TRUE':
			self.match('TRUE')
			# return('TRUE')
		elif self.la=='FALSE':
			self.match('FALSE')
			# return('FALSE')
		else:
			raise ParseError("in boolean: TRUE or FALSE expected")


	def orop(self):
		if self.la=='OR':
			self.match('OR')
			# return('or')
		else:
			raise ParseError("in orop: or expected")

	def andop(self):
		if self.la=='AND':
			self.match('AND')
			# return('and')
		else:
			raise ParseError("in andop: and expected")

	def notop(self):
			if self.la=='NOT':
				self.match('NOT')
				# return('not')
			elif self.la==')' or self.la=='VARIABLE' or self.la=='TRUE' or self.la=='FALSE': #From follow set
				return
			elif self.la is None:
				return
			else:
				raise ParseError("in notop : not expected")

# the main part of prog

# create the parser object
parser = MyParser()

# open file for parsing
with open("myparser.txt","r") as fp:

	# parse file
	try:
		parser.parse(fp)
	except plex.errors.PlexError:
		_,lineno,charno = parser.position()	
		print("Scanner Error: at line {} char {}".format(lineno,charno+1))
	except ParseError as perr:
		_,lineno,charno = parser.position()	
		print("Parser Error: {} at line {} char {}".format(perr,lineno,charno+1))
