import putio
import xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.putiov2')
__lang__ = __settings__.getLocalizedString


class PutioAuthFailureException(Exception):
    """An authentication error occured."""

    def __init__(self, header, message, duration=10000, icon='error.png'):
        self.header = header
        self.message = message
        self.duration = duration
        self.icon = icon


class PutioApiHandler(object):
    """A Put.io API client helper."""

    def __init__(self, oauth2_token):
        if not oauth2_token:
            raise PutioAuthFailureException(header=__lang__(30001), message=__lang__(30002))
        self.client = putio.Client(oauth2_token)

    def get(self, id_):
        return self.client.File.get(id_)

    def list(self, parent=0):
        items = []
        for item in self.client.File.list(parent_id=parent):
            if item.content_type and self.is_showable(item):
                items.append(item)
        return items

    def is_showable(self, item):
        if item.is_audio or item.is_video or item.is_folder:
            return True
        return False