r"""
Строим дерево доменных имен:

                     [root]
                 /             \
               com              ru
            /      \         /       \
        l2-0      l2-1    l2-2      l2-3
    /    |   \              |         |
 l3-0 l3-1 l3-2           l3-3      l3-4

 Если у узла есть листья - группируем.
 *.com
 *.l2-0.com
 *.l2-2.ru
 *.l2-3.ru
 Можно реализовать частный случай для единственного листа.
"""
import typing


class DomainNode:
    def __init__(self, name: str):
        self.__name = name
        self._children: dict[str, 'DomainNode'] = dict()

    @property
    def is_leaf(self) -> bool:
        return not self._children

    @property
    def leafs(self) -> typing.Generator['DomainNode', None, None]:
        yield from (leaf
                    for leaf in self._children.values()
                    if leaf.is_leaf)

    @property
    def nodes(self) -> typing.Generator['DomainNode', None, None]:
        yield from (node
                    for node in self._children.values()
                    if not node.is_leaf)

    def fill_tree(self, nodes: list[str]):
        if not nodes:
            return

        top_domain = nodes.pop()
        if top_domain not in self._children:
            self._children[top_domain] = DomainNode(top_domain)

        self._children[top_domain].fill_tree(nodes)

    def group_leafs(self, prefix: list[str]) \
            -> typing.Generator[list[str], None, None]:
        current_domain = prefix + [self.__name]

        leafs_count = sum(1 for _ in self.leafs)
        if leafs_count:
            yield current_domain

        for node in self.nodes:
            yield from node.group_leafs(current_domain)

    def __iter__(self):
        yield from self._children.values()


class Root(DomainNode):
    def __init__(self):
        super().__init__("")

    def add(self, domain: str):
        self.fill_tree(domain.split("."))

    def compact_tree(self) -> typing.Generator[str, None, None]:
        for l1_domain in self._children.values():
            yield from (".".join(reversed(grouped_domain))
                        for grouped_domain
                        in l1_domain.group_leafs(list()))
