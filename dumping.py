import datetime
import hashlib
import copy

class Block:
    version = 1.0
    target = 3
    def __init__(self, previous_hash,data):
        self.previous_hash = previous_hash
        self.data = data
        #self.merkle_root = self.get_merkle_root(self.data)
        self.time =  datetime.datetime.now()
        self.nonce = 0
        self.get_hash()
    #def get_merkle_root(self,data):
    def get_hash(self):
        string_to_hash = "".join(self.data) + str(self.previous_hash) + str(self.nonce)+str(self.time)
        self.hash = hashlib.sha256(string_to_hash.encode()).hexdigest()
        return self.hash

class Block_Chain:
    network = [Block('0000',"this is empty block")]
    def __init__(self):
        self.chain = copy.deepcopy(Block_Chain.network)
        self.chain_length = len(self.chain)
        
    def pow(self, Blocks):
        C_Block = copy.deepcopy(Blocks)
        print("<채굴중...>")
        for i in range(1000000000):
            C_Block.nonce = i
            C_Block.hash = C_Block.get_hash()
            msg = '\r현재 논스: %s 현재 해쉬: %s' % (i,C_Block.hash)
            print('' * len(msg), end='')
            print(msg, end='')
            if C_Block.hash[:C_Block.target] == '0'*C_Block.target:
                return i
    
    def add(self,Blocks):
        result = self.pow(Blocks)
        Blocks.nonce = result
        Blocks.hash = Blocks.get_hash()
        self.chain.append(Blocks)
        return result
    
    def compare(self,Blocks,nonce):
        C_Block = copy.deepcopy(Blocks)
        C_Block.nonce = nonce
        if C_Block.hash[:C_Block.target] == '0'*C_Block.target:
            return 1
        else:
            return 0
        
    
    def get_previous_hash(self,chain):
        for i in range(len(chain)):
            if i == 0:
                continue
            else:
                chain[i].previous_hash = chain[i-1].hash
                chain[i].hash = chain[i].get_hash()
        return chain[len(chain)-1].hash

class Account:
    accounts = []
    def __init__(self,name):
        Account.accounts.append(self)
        self.name = name
        self.chain = Block_Chain()
        self.coin = 0
        self.noce = None
        self.new_blocks = None
    def new_block(self, data):
        print("채굴자: %s     보유코인: %d"%(self.name,self.coin))
        print("target: %s"%(Block.target))
        self.new_blocks = Block(self.chain.get_previous_hash(self.chain.chain),data)
        self.nonce = self.chain.add(self.new_blocks)
    
    def consensus(self):
        limit = len(Account.accounts)/2
        sum = 0
        for i in range(len(Account.accounts)):
            if Account.accounts[i].chain.compare(self.new_blocks,self.nonce) == 1:
                sum+=1
        if sum>=limit:
            self.coin += 1
            Block_Chain.network.append(self.new_blocks)
            for i in range(len(Account.accounts)):
                Account.accounts[i].chain.chain = copy.deepcopy(Block_Chain.network)
            print("\n채굴이 완료되었습니다.\n")
while True:
    print("<Dumping_Coin>\n옵션을 선택하세요\n1.계정 생성  2.채굴하기  3.블록체인 상태보기  4.끝내기")
    a = input("입력: ")
    if int(a) == 1:
        name = input("사용자 이름을 입력하세요: ")
        Account(name)
    elif int(a) == 2:
        print("다음 중 채굴에 사용할 계정을 선택해 주세요")
        for i in range(len(Account.accounts)):
            print("%d.%s"%(i+1,Account.accounts[i].name),end=" ")
        name = input("\n사용할 계정 번호: ")
        name = int(name)
        name-=1
        Account.accounts[name].new_block("안녕하세요")
        Account.accounts[name].consensus()
    elif int(a) == 3:
        print("<계정 정보>")
        for i in range(len(Account.accounts)):
            print("----------------------------------------------------------------------------")
            print("계정 번호: %d\n계정 이름:%s\n보유 코인: %d\n마지막 블럭 해쉬: %s"%(i,Account.accounts[i].name,Account.accounts[i].coin,Account.accounts[i].chain.chain[len(Account.accounts[i].chain.chain)-1].hash))
            if i == len(Account.accounts)-1:
                print("----------------------------------------------------------------------------")
        print("<블록체인 정보>")
        for i in range(len(Block_Chain.network)):
            print("----------------------------------------------------------------------------")
            print("블럭 번호: %d\n이전 해쉬: %s\n논스: %s\n데이터: %s\n현재 해쉬: %s"%(i,Block_Chain.network[i].previous_hash,Block_Chain.network[i].nonce,Block_Chain.network[i].data,Block_Chain.network[i].hash))
            if i == len(Block_Chain.network)-1:
                print("----------------------------------------------------------------------------")
    else:
        print("블록체인 네트워크를 종료합니다.")
        break
