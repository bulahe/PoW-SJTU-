class MiningSimulator:
    def __init__(self, nodes, rounds, malicious_node):
        self.nodes = nodes                          # 节点列表
        self.rounds = rounds                        # 挖矿轮数
        self.global_block_id = 1                    # 全局唯一的区块 ID
        self.world_length = 0                       # 当前最长链的区块数
        self.preBlock = 0                           # 当前最长链的最后一个区块
        self.success_rates = []                     # 存储每轮的出块成功率
        self.growth_speeds = []                     # 存储每轮的增长速度
        self.malicious_nodes = malicious_node       # 恶意节点列表
        self.malicious_blocks = []                  # 存储恶意节点生成的区块
        # 新增统计变量
        self.fork_attack = 0
        self.fork_attack_successes = 0              # 成功的分叉攻击次数
        self.selfish_mining_time = 0             # 自私挖矿收益的区块数    
    def run_simulation(self):
        for round_num in range(self.rounds):
            round_blocks = []        # 本轮生成的区块
            isCreateblock = False
            isCreateMblock = False
            # 每个节点尝试出块
            for node in self.nodes:
                new_block = node.mine_block(self.world_length, self.global_block_id, self.preBlock)
                if new_block:
                    round_blocks.append(new_block)
                    self.global_block_id += 1
                    isCreateblock = True
                    a_block = new_block
                    # 输出新区块的内容
                    print(
                        f"New Block Created: "
                        f"block id: {new_block.block_id:<3} "
                        f"node id: {new_block.node_id:<8} "
                        f"previous block id: {new_block.previous_block:<3} "
                        f"length: {new_block.length:<3}"
                    )
            # 计算恶意节点出块 
            for mnode in self.malicious_nodes:
                if self.malicious_blocks:  # 如果已经有恶意节点的链
                    new_mblock = mnode.mine_block(mnode_point, self.global_block_id, preMblock)
                    if new_mblock:
                        self.global_block_id += 1
                        self.malicious_blocks.append(new_mblock)
                        print(f"恶意节点挖出第 {mnode_point+1} 块")
                        isCreateMblock = True
                        preMblock = new_mblock.block_id
                        self.selfish_mining_time += 1
                        break
                else:
                    # 恶意节点创建新的私有链
                    new_mblock = mnode.mine_block(self.world_length, self.global_block_id, self.preBlock)
                    if new_mblock:
                        self.global_block_id += 1
                        self.malicious_blocks.append(new_mblock)
                        print("攻击开始")
                        self.fork_attack += 1
                        node_point = 0
                        mnode_point = 0
                        isCreateMblock = True
                        preMblock = new_mblock.block_id
                        break
            # 判断恶意节点生成区块是否成功取代普通节点
            if self.malicious_blocks:
                if isCreateblock:
                    node_point += 1
                if isCreateMblock:
                    mnode_point += 1    
                if node_point == 6:
                    print("恶意节点攻击失败")
                    node_point = 0
                    mnode_point = 0
                    self.malicious_blocks = []
                if mnode_point == 6:
                    print("恶意节点攻击成功")
                    self.world_length += mnode_point - node_point
                    self.preBlock = preMblock
                    node_point = 0
                    mnode_point = 0
                    self.malicious_blocks = [] 
                    isCreateblock = False 
                    
                    # 更新分叉攻击成功次数
                    self.fork_attack_successes += 1
                    
            # 更新最长链和前一个区块
            if isCreateblock:
                self.world_length = a_block.length
                self.preBlock = a_block.block_id
            # 计算并存储本轮的出块成功率和增长速度
            success_rate = len(round_blocks) / len(self.nodes) if self.nodes else 0
            growth_speed = len(round_blocks)
            self.success_rates.append(success_rate)
            self.growth_speeds.append(growth_speed)
    def print_results(self):
        # 计算总的平均出块成功率和增长速度
        average_success_rate = sum(self.success_rates) / self.rounds if self.rounds else 0
        average_growth_speed = sum(self.growth_speeds) / self.rounds if self.rounds else 0
        # 计算分叉攻击成功率和自私挖矿收益比例
        fork_attack_success_rate = self.fork_attack_successes / self.fork_attack if self.fork_attack else 0
        selfish_mining_reward_ratio = self.fork_attack_successes*6 / self.selfish_mining_time if self.selfish_mining_time else 0
        print(f"平均出块成功率: {average_success_rate:.2%}")
        print(f"平均增长速度: {average_growth_speed:.3f} 个区块/轮")
        print(f"分叉攻击成功率: {fork_attack_success_rate:.2%}")
        print(f"自私挖矿收益比例: {selfish_mining_reward_ratio}")