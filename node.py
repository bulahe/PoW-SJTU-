import random
from block import Block
class Node:
    def __init__(self, node_id, block_success_rate):
        self.node_id = node_id                 # 节点 ID
        self.block_success_rate = block_success_rate  # 出块成功概率

    def mine_block(self, world_length, global_block_id,preblock):
        """按出块概率生成区块，添加到公共链"""
        if random.random() < self.block_success_rate:
            new_block = Block(global_block_id, self.node_id, preblock,world_length)#这个block的id，挖到这个block的节点id，上一个block的id
            return new_block
        return None