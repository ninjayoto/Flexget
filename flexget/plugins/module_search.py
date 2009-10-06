import logging
from flexget.plugin import *

__pychecker__ = 'unusednames=parser'

log = logging.getLogger('search')

class Search:
    """
        Search entry from sites. Accepts list of known search plugins, list is in priority order.
        Once hit has been found no more searches are performed. Should be used only when
        there is no other way to get working download url, ie. when input plugin does not provide 
        any downloadable urls.
        
        Example:
        
        search:
          - newtorrents
          - piratebay
          
        Notes: 
        - Some resolvers will use search plugins automaticly if enry url points into a search page.
    """
    def validator(self):
        # TODO: should only accept registered search plugins
        from flexget import validator
        search = validator.factory('list')
        search.accept('text')
        return search

    def on_feed_resolve(self, feed):
        # no searches in unit test mode
        if feed.manager.unit_test: 
            return 
        
        plugins = {}
        for plugin in get_plugins_by_group('search'):
            plugins[plugin.name] = plugin.instance
            
        for entry in feed.entries:
            found = False
            # loop trough configured searches
            for name in feed.config.get('search', []):
                if not name in plugins:
                    log.error('Search plugins %s not found' % name)
                    log.debug('Registered: %s' % ', '.join(plugins.keys()))
                    continue
                else:
                    log.debug('Issuing search from %s' % name)
                    url = plugins[name].search(feed, entry)
                    if url:
                        log.debug('Found url: %s' % url)
                        entry['url'] = url
                        found = True
                        break
            # failed
            if not found:
                feed.reject(entry, 'search failed')

register_plugin(Search, 'search')