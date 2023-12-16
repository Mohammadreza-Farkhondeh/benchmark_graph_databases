import pydgraph

class DgraphClient:
    def __init__(self, host: str, port: int, username: str, password: str, namespace: str) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.namespace = namespace
        self.uri = f'{host}:{port}'
        self.client_stub = pydgraph.DgraphClientStub(self.uri)
        self.client = pydgraph.DgraphClient(self.client_stub)

        def create_node(self, id: str) -> str:
            """Create a vertex with givern id
            Args:
                id (int): the vertex id
            """
            pass

        def create_edge(self, source: str, target: str) -> str:
            """Create an edge between two vertices with givern ids
            Args:
                source (int): the source vertex id
                target (int): the target vertex id
            """
            pass

        def __exit__(self):
            pass
