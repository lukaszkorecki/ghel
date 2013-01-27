import xml.dom.minidom as minidom
import urwid

class Events:
	@classmethod
	def loadFromFile(self, path):
		""" Convinence method for loading the feed from given file """
		xml = open(path).read()
		feed = minidom.parseString(xml)
		return self(feed)

	def __init__(self, xml):
		self.dom_feed = xml

	def extractEvents(self):
		""" Parse xml and extract required informatio from feed. Returns a list of tuples (titile, author,published, url) """
		entries = self.dom_feed.getElementsByTagName('entry')
		events = []
		for entry in entries:
			title = self.getText(self.getElement(entry, 'title'))
			published = self.getText(self.getElement(entry, 'published'))
			author = self.getText(self.getElement(self.getElement(entry,'author'), 'name'))

			url = self.getElement(entry, 'link').attributes['href'].value

			events.append((title, author, published, url))

		return events

	def getElement(self, node, tag):
		return node.getElementsByTagName(tag)[0]

	def getText(self,element):
		return element.firstChild.toprettyxml()

path = "/Users/lukaszkorecki/Desktop/lukaszkorecki.private.atom.xml"

for event in Events.loadFromFile(path).extractEvents():
	print "Title: {0} Author: {1} Published: {2} url: {3}".format(*event)
