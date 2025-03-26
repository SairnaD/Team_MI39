class Node:
    id_counter = 0

    def __init__(self, sequence, player_score=0, ai_score=0, turn=1, depth=0):
        self.sequence = sequence
        self.player_score = player_score
        self.ai_score = ai_score
        self.turn = turn
        self.depth = depth
        self.id = Node.id_counter
        Node.id_counter += 1
        self.children = []
        self.value = None
        self.evaluated = False

    def make_move(self, i):
        sum_val = self.sequence[i] + self.sequence[i + 1]

        if sum_val > 7:
            self.sequence[i] = 1
            if self.turn == 1:
                self.player_score += 1
            else:
                self.ai_score += 1
        elif sum_val < 7:
            self.sequence[i] = 3
            if self.turn == 1:
                self.player_score -= 1
            else:
                self.ai_score -= 1
        else:
            self.sequence[i] = 2
            self.player_score += 1
            self.ai_score += 1

        del self.sequence[i + 1]
        self.turn *= -1

    def get_children(self):
        for i in range(len(self.sequence) - 1):
            new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn, self.depth + 1)
            new_node.make_move(i)
            self.children.append(new_node)
        return self.children

    def evaluate(self):
        if self.evaluated:
            return

        if len(self.children) == 0:
            if self.player_score > self.ai_score:
                self.value = -1 
            elif self.player_score < self.ai_score:
                self.value = 1
            else:
                self.value = 0
        else: 
            if self.depth % 2 == 0:
                max_val = float('-inf')
                for child in self.children:
                    child.evaluate()
                    max_val = max(max_val, child.value)
                self.value = max_val
            else:
                min_val = float('inf')
                for child in self.children:
                    child.evaluate()
                    min_val = min(min_val, child.value)
                self.value = min_val
        self.evaluated = True
        
    def evaluate_state(self):
        score_difference = self.ai_score - self.player_score

        sequence_score = sum(1 if num in [1, 2] else -1 for num in self.sequence)

        return score_difference + sequence_score


    def minimax(self, depth, maximizing_player):
        if depth == 0 or len(self.sequence) == 1:
            return self.evaluate_state()
        
        if maximizing_player:
            max_eval = float('-inf')
            for i in range(len(self.sequence) - 1):
                new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn, self.depth + 1)
                new_node.make_move(i)
                eval = new_node.minimax(depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(len(self.sequence) - 1):
                new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn, self.depth + 1)
                new_node.make_move(i)
                eval = new_node.minimax(depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or len(self.sequence) == 1:
            return self.evaluate_state()
        
        if maximizing_player:
            max_eval = float('-inf')
            for i in range(len(self.sequence) - 1):
                new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn, self.depth + 1)
                new_node.make_move(i)
                eval = new_node.alpha_beta(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(len(self.sequence) - 1):
                new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn, self.depth + 1)
                new_node.make_move(i)
                eval = new_node.alpha_beta(depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
        
    def find_best_move(self, method="alpha-beta"):
        best_move = None
        best_value = float('-inf') if self.turn == -1 else float('inf')

        for i in range(len(self.sequence) - 1):
            new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn, self.depth + 1)
            new_node.make_move(i)

            if method == "minimax":
                move_value = new_node.minimax(3, self.turn == -1)
            elif method == "alpha-beta":
                move_value = new_node.alpha_beta(3, float('-inf'), float('inf'), self.turn == -1)

            if self.turn == -1:
                if move_value > best_value:
                    best_value = move_value
                    best_move = i
            else: 
                if move_value < best_value:
                    best_value = move_value
                    best_move = i

        return best_move


    
    def to_string(self):
        return f"Node {self.id} | Sequence: {self.sequence} | Depth: {self.depth}"

    def to_string_smooth(self):
        if self.ai_score > self.player_score:
            value = 1
        elif self.ai_score < self.player_score:
            value = -1
        else:
            value = 0 

        children_str = ", ".join(str(child.sequence) for child in self.children)
        return f"Sequence: {self.sequence} | Player Score: {self.player_score} | AI Score: {self.ai_score} | Children: [{children_str}]"

