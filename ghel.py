import xml.dom.minidom as minidom


class Events:
	def __init__(self, xml):
		self.dom_feed = xml

	def extractEvents(self):
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



xml = open("/Users/lukaszkorecki/Desktop/lukaszkorecki.private.atom.xml").read()
feed = minidom.parseString(xml)
for event in Events(feed).extractEvents():
	print "Title: {0} Author: {1} Published: {2} url: {3}".format(*event)
