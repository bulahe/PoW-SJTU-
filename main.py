from node import Node
from simulator import MiningSimulator
def main():
    # 参数设置
    node_count = 60            
    # 节点数量
    block_success_rate = 0.003  # 出块成功概率
    rounds = 100000               # 挖矿轮数
    malicious_node_count = 40
    # 初始化节点
    nodes = [Node(f"node{i}", block_success_rate) for i in range(node_count)]
    malicious_node = [Node(f"node{i}", block_success_rate) for i in range(malicious_node_count)]
    # 创建挖矿模拟器
    simulator = MiningSimulator(nodes, rounds,malicious_node)
    # 运行模拟
    simulator.run_simulation()
    # 输出结果
    simulator.print_results()
if __name__ == "__main__":
    main()