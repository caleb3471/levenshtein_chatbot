import pandas as pd


# 챗봇 클래스 생성 
class SimpleChatBot:
    
    #상속과 동시에 파일에서 질문과 답변을 분리해서 변수생성
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)
        
    #CSV파일을 읽어서 질문과 답변으로 분리하여 return
    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()
        answers = data['A'].tolist()
        return questions, answers
    
    #문자열 두개를 입력받아 두개의 레베슈타인 거리계산
    def calc_distance(self, a, b):
        ''' 레벤슈타인 거리 계산하기 '''
        if a == b: return 0 # 같으면 0을 반환
        a_len = len(a) # a 길이
        b_len = len(b) # b 길이
        if a == "": return b_len
        if b == "": return a_len
        # 2차원 표 (a_len+1, b_len+1) 준비하기 --- (※1)
        # matrix 초기화의 예 : [[0, 1, 2, 3], [1, 0, 0, 0, 0], [2, 0, 0, 0, 0], [3, 0, 0, 0, 0], [4, 0, 0, 0, 0]]
        # [0, 1, 2, 3]
        # [1, 0, 0, 0]
        # [2, 0, 0, 0]
        # [3, 0, 0, 0] 
        matrix = [[] for i in range(a_len+1)] # 리스트 컴프리헨션을 사용하여 1차원 초기화
        for i in range(a_len+1): # 0으로 초기화
            matrix[i] = [0 for j in range(b_len+1)]  # 리스트 컴프리헨션을 사용하여 2차원 초기화
        # 0일 때 초깃값을 설정
        for i in range(a_len+1):
            matrix[i][0] = i
        for j in range(b_len+1):
            matrix[0][j] = j
        # 표 채우기 --- (※2)
        # print(matrix,'----------')
        for i in range(1, a_len+1):
            ac = a[i-1]
            # print(ac,'=============')
            for j in range(1, b_len+1):
                bc = b[j-1] 
                # print(bc)
                cost = 0 if (ac == bc) else 1  #  파이썬 조건 표현식 예:) result = value1 if condition else value2
                matrix[i][j] = min([
                    matrix[i-1][j] + 1,     # 문자 제거: 위쪽에서 +1
                    matrix[i][j-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                    matrix[i-1][j-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
            ])
            # print(matrix)
        # print(matrix,'----------끝')
        return matrix[a_len][b_len]
    
    #입력 문자열을 질문 리스트에 질문과 레베슈타인거리를 계산하여 가장 비슷한 질문의 인덱스를 반환
    def re_levenshtein(self,input_text):
        best_index=0
        best_score=[]
        que_len=len(self.questions)
      
        
        for i in range(0, que_len):
            score=self.calc_distance(self.questions[i], input_text)
            best_score.append(score)
            if min(best_score) >= score:
                best_index = i
            else:
                pass
            
        return best_index
    #가장 비슷한 질문의 인덱스의 답변을 반환    
    def find_best_answer(self, input_sentence):
        best_index=self.re_levenshtein(input_sentence)
        return self.answers[best_index]
        
# 데이터 파일의 경로를 지정
filepath = 'ChatbotData.csv'

# 클래스 상속
chatbot = SimpleChatBot(filepath) 

#질문이 종료가 입력되기 전 까지 반복 
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    else:
        response = chatbot.find_best_answer(input_sentence)
        print('Chatbot:', response)
