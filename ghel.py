import xml.dom.minidom as minidom
import urwid

class Events:
	@classmethod
	def loadFromFile(cls, path):
		""" Convinence method for loading the feed from given file """
		xml = open(path).read()
		feed = minidom.parseString(xml)
		return cls(feed)

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

class UI:

	def eventList(self, title, events):
		""" builds the menu out of lines of text """
		body = [urwid.Text(title), urwid.Divider()]
		for event in events:
			button = urwid.Button(event[0])
			body.append(urwid.AttrMap(button, None, focus_map='reversed'))
		return urwid.ListBox(urwid.SimpleFocusListWalker(body))


path = "/Users/lukaszkorecki/Desktop/lukaszkorecki.private.atom.xml"

events  = Events.loadFromFile(path).extractEvents()


main = urwid.Padding(UI().eventList("GH feed", events ), left=2, right=0)
urwid.MainLoop(main, palette=[('reversed', 'standout', '')]).run()
