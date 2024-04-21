from arbol_model import ArbolModel
import graphviz

class BodyController:
    def __init__(self):
        self.root = None

    def insert_body(self, value):
        self.root = self._insert_body(self.root, value)

    def _insert_body(self, root, value):
        if root is None:
            return ArbolModel(value)
        elif value.bodyId < root.value.bodyId:
            root.left = self._insert_body(root.left, value)
        elif value.bodyId > root.value.bodyId:
            root.right = self._insert_body(root.right, value)

        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        balance = self._get_balance(root)

        # Rotaciones para balancear el árbol
        if balance > 1 and value.bodyId < root.left.value.bodyId:
            return self._rotate_right(root)
        if balance < -1 and value.bodyId > root.right.value.bodyId:
            return self._rotate_left(root)
        if balance > 1 and value.bodyId > root.left.value.bodyId:
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)
        if balance < -1 and value.bodyId < root.right.value.bodyId:
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)

        return root


    def _get_height(self, root):
        if root is None:
            return 0
        return root.height

    def _get_balance(self, root):
        if root is None:
            return 0
        return self._get_height(root.left) - self._get_height(root.right)

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def get_body(self, value):
        return self._get_body(self.root, value)

    def _get_body(self, root, value):
        if root is None:
            return None
        elif value == root.value.bodyId:
            return root.value
        elif value < root.value.bodyId:
            return self._get_body(root.left, value)
        elif value > root.value.bodyId:
            return self._get_body(root.right, value)


    def generar_arbol_grafico(self):
        dot = graphviz.Digraph()
        self._generar_arbol_grafico(self.root, dot)

        archivo_salida = "arbol.dot"
        dot.render(archivo_salida, format='png', cleanup=True)

    def _generar_arbol_grafico(self, nodo, dot):
        if nodo is not None:
            dot.node(str(nodo.value.bodyId))
            if nodo.left is not None:
                dot.edge(str(nodo.value.bodyId), str(nodo.left.value.bodyId))
                self._generar_arbol_grafico(nodo.left, dot)
            if nodo.right is not None:
                dot.edge(str(nodo.value.bodyId), str(nodo.right.value.bodyId))
                self._generar_arbol_grafico(nodo.right, dot)

    def clear_db(self):
        self.root = None













