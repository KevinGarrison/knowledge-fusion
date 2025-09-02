from toolbox_langchain import ToolboxClient

class GoogleMCPtoolbox:
    def __init__(self, url="http://127.0.0.1:5000"):
        self.url = url
        self.client = None
        self.tools = None

    def __enter__(self):
        self.client = ToolboxClient(self.url)
        self.client.__enter__()     # open client
        self.tools = self.client.load_toolset()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.__exit__(exc_type, exc_val, exc_tb)