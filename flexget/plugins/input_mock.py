import logging
from flexget.feed import Entry
from flexget.plugin import *

log = logging.getLogger('input_mock')

class InputMock:
    """
        Allows adding mock input entries. Example:
        
        input_mock:
          - {title: foobar, url: http://some.com }
          - {title: mock, url: http://another.com }
    """
    def validator(self):
        from flexget import validator
        container = validator.factory('list')
        entry = container.accept('dict')
        entry.accept('url', key='url')
        entry.accept('text', key='title', required=True)
        entry.accept_any_key('text')
        entry.accept_any_key('number')
        return container

    def on_feed_input(self, feed):
        config = feed.config.get('input_mock', [])
        for line in config:
            entry = Entry()
            for k,v in line.iteritems():
                entry[k] = v
            # no url specified, add random one (ie. test)
            if not 'url' in entry:
                import string
                import random
                entry['url'] = 'http://localhost/mock/%s' % ''.join([random.choice(string.letters+string.digits) for x in range(1, 30)])
            feed.entries.append(entry)

register_plugin(InputMock, 'input_mock', debug=True)
