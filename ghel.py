import xml.dom.minidom as minidom
import os
import popen2
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

			url = self.getElement(entry, 'link').attributes['href'].value.strip()

			events.append((title, author, published, url))

		return events

	def getElement(self, node, tag):
		return node.getElementsByTagName(tag)[0]

	def getText(self,element):
		return element.firstChild.toprettyxml().strip()

class UI:

	def __init__(self, events):
		self.events = events

	def event_list(self, title, events):
		""" builds the menu out of lines of text """
		body = [urwid.Text(title), urwid.Divider()]
		for event in events:
			button = urwid.Button(self.print_event(event))
			urwid.connect_signal(button, 'click', self.item_chosen, event)
			body.append(urwid.AttrMap(button, None, focus_map='reversed'))

		return urwid.ListBox(urwid.SimpleFocusListWalker(body))

	def main(self, title):

		self.main = urwid.Padding(self.event_list(title, self.events ), left=0, right=0)
		return self.main

	def print_event(self, event):
		return "{1}: {0} @ {2}".format(*event)

	def item_chosen(self, button, event):
		popen2.popen3("open '{0}'".format(event[3]))
		return



path = "/Users/lukaszkorecki/Desktop/lukaszkorecki.private.atom.xml"

events  = Events.loadFromFile(path).extractEvents()


urwid.MainLoop(UI(events).main("GH feed"), palette=[('reversed', 'standout', '')]).run()
