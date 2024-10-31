class Block:
    def __init__(self, block_id, node_id, previous_block=None,world_length=0):
        self.block_id = block_id        # 当前块的 ID
        self.node_id = node_id          # 生成该块的节点 ID
        self.previous_block = previous_block  # 上一个区块的引用
        self.length = world_length+1