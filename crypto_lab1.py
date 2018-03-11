import math
import random


class CryptoLab1_1:
    def __init__(self, a, c, m, seed, length):
        self.a = a
        self.c = c
        self.m = m
        self.x = seed
        self.length = max(5, math.floor(length))
        self.s=[]

    def lcg(self):
        self.x = (self.x*self.a+self.c)%self.m
        return self.x
    
    def predict(self):
        self.prepare_random_values()
        self.m1 = self.guess_modulus()
        self.a1 = self.guess_multiplier()
        self.c1 = self.guess_increment()
        predicted_value = (self.s[self.length-1]*self.a1+self.c1)%self.m1
        actual_value = self.lcg()
        #print('Prediction: '+str(predicted_value)+'\nActual: '+str(actual_value))
        return predicted_value==actual_value
    
    def prepare_random_values(self):
        self.s = []
        for i in range(self.length):
            self.s.append(self.lcg())
    
    def guess_modulus(self):
        guessed_modulus = 0
        for i in range(self.length-3):
            temp = abs((self.s[i+1]-self.s[i])*(self.s[i+3]-self.s[i+2])-(self.s[i+2]-self.s[i+1])**2)
            guessed_modulus = math.gcd(guessed_modulus, temp)
        return max(guessed_modulus,1)
    
    def guess_multiplier(self):
        for i in range(self.length-2):
            i_m=self.inverse_modulo((self.s[i+1]-self.s[i]+self.m1)%self.m1, self.m1)
            if i_m!=-1:
                return (self.s[i+2]-self.s[i+1])*i_m
        return 1
        
    def inverse_modulo(self, a, n):
        new_t = 1; old_t = 0
        new_r = a; old_r = n
        while new_r!=0:
            quotient=old_r//new_r
            old_t, new_t = new_t, old_t-quotient*new_t 
            old_r, new_r = new_r, old_r-quotient*new_r 
        if old_r>1:
            return -1
        return (old_t+n)%n
    
    def guess_increment(self):
        return self.s[1]-self.s[0]*self.a1


class CryptoLab1_2:
    def __init__(self, seed):
        self.r=[seed]
        for i in range(30):
            self.r += [self.r[-1]*16807%2147483647]
        for i in range(3):
            self.r += [self.r[-31]]
        for i in range(310):
            self.r += [(self.r[-3]+self.r[-31])%4294967296]
            
    def glibc_random(self):
        self.r += [(self.r[-3]+self.r[-31])%4294967296]
        return self.r[-1]>>1
    
    def prepare_random_values(self):
        self.o=[]
        for i in range(31):
            self.o.append(self.glibc_random())
    
    def predict(self):
        self.prepare_random_values()
        predicted_value = (self.o[-31]+self.o[-3])%2147483648
        actual_value = self.glibc_random()
        #print('Prediction: '+str(predicted_value)+'\nActual: '+str(actual_value))
        return predicted_value==actual_value
    
        
def test_predictions(test_number):
    s1=s2=0
    for i in range(test_number):
        #p = CryptoLab1_1(random.randint(1,2**32),random.randint(1,2**32),104729,random.randint(1,2**32),100)
        p = CryptoLab1_1(random.randint(1,2**32),random.randint(1,2**32),2*random.randint(1,2**32)-1,random.randint(1,2**32),100)
        s1 += p.predict()
        q = CryptoLab1_2(random.randint(1,2**32))
        s2 += q.predict()
    print('LCG:   '+str(s1/test_number)+'\nGLIBC: '+str(s2/test_number))
    
test_predictions(1000)