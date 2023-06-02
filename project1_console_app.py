import os
import requests
import re


class DFA(): #DFA main class
    current_state=""

    def __init__(self ,states ,alphabet ,transition ,s_state ,f_states):
        if not isinstance(states ,tuple)or not isinstance(s_state ,str) or not isinstance(f_states ,set):
            raise  Exception("Wrong arguments format for DFA.")

        self.states = states
        self.alphabet = set(alphabet)
        self.transition = transition
        self.transition2 = dict()
        self.s_state = s_state
        self.f_states = f_states

        for state in states:
            self.transition2[state] = dict()

        for trans in transition:
            for alpha in trans[2]:
                self.transition2[trans[0]][alpha] = trans[1]

        self.trap_states = self.find_traps()

    def __str__(self):
        string = "M = (Q ,Sigma ,Delta ,q0 ,F)\n"
        string += "Q : " + str(self.states) + '\n' + "Sigma : " + str(self.alphabet) + '\n'
        string +=  "Delta : " + str(self.transition) + '\n' + "Starting state : " + str(self.s_state) + '\n'
        string +=  "F : " + str(self.f_states) + '\n'
        return string

    def run(self ,text): #Runs DFA from start state
        self.current_state = self.s_state

        out_size = 0
        for char in text:
            # if char not in self.alphabet: #if input doesnt belong to alphabet
            #     return (False ,out_size)
            flag = bool(True)
            for trans in self.transition:
                if trans[0] == self.current_state and char in trans[2]:
                    if self.current_state in self.f_states and trans[1] in self.trap_states:
                        return (True ,out_size)
                    self.current_state = trans[1]
                    out_size += 1
                    flag = False
                    break
            if flag: #if FA couldn't consume input character
                return (False ,out_size)
            if self.trap_states and self.current_state in self.trap_states: #if FA is trapped
                return (False ,out_size-1)

        if self.current_state in self.f_states: #wether FA is in final states or not
            return (True ,out_size)
        else:
            return (False ,out_size)

    # def run2(self ,text):
    #     self.current_state = self.s_state

    #     out_size = 0
    #     for char in text:
    #         # if char not in self.alphabet: #if input doesnt belong to alphabet
    #         #     return (False ,out_size)
    #         try:
    #             self.current_state = self.transition2[self.current_state][char]
    #             out_size += 1

    #         except: #FA couldn't consume input character
    #             return (False ,out_size)

    #         if self.trap_states and self.current_state in self.trap_states: #if FA is trapped
    #             return (False ,out_size-1)

    #     if self.current_state in self.f_states: #Wether FA is in final states or not
    #         return (True ,out_size)
    #     else:
    #         return (False ,out_size)

    def run2(self ,text): #Runs DFA from start state with Dictionary style transition function
        self.current_state = self.s_state

        consumed = 0
        final_size = 0
        for char in text:
            # if char not in self.alphabet: #if input doesnt belong to alphabet
            #     return (False ,out_size)
            try:
                self.current_state = self.transition2[self.current_state][char]
                consumed += 1

            except: #FA couldn't consume input character
                return (False ,final_size)

            if self.trap_states and self.current_state in self.trap_states: #if FA is trapped
                return (False ,consumed-1)

            if self.current_state in self.f_states: 
                final_size = consumed

        if self.current_state in self.f_states: #Wether FA is in final states or not
            return (True ,final_size)
        else:
            return (False ,final_size)

    def find_traps(self): #looks for traps
        trap_states = set()

        for state in self.states:
            flag = False
            for trans in self.transition:
                if trans[0] == state:
                    if trans[0] == trans[1] and trans[0] not in self.f_states:
                        flag = True
                    else:
                        flag = False
                        break
                else:
                    continue
            if flag:
                trap_states.add(state)
        return trap_states


clr=False
def clear():  # waits for an input then clears the screen
    global clr
    if clr:
        input("\nPress ENTER key to continue")
    os.system("cls")
    clr=True

def get_response(url): #requests response from given URL
    try:
        return requests.get(url)
    except:
        return None

def search(dfa ,text): #calls (DFA).run() for each input charachter till the end of input each time
    # results = list()
    j=0
    while j < len(text):
        i = dfa.run2(text[j: ])[1] #i is how many charcters were accepted by DFA after last passage from final state
        if i:
            # results.append(text[j : j+i])
            yield text[j : j+i]
            j+=i
                
        j+=1

    # return results

def search_sec_dep(engine ,urls ,eng_type="dfa"): #searchs for emails in found URLs
    if not urls:
        return []

    new_emails = set()
    for url in urls:
        res = get_response(url)
        if res:
            text = res.text
            if eng_type.lower() == "dfa":
                for new_email in search(engine ,text):
                    new_emails.add(new_email)
            elif eng_type.lower() == "re":
                for new_email in engine.findall(text):
                    new_emails.add(new_email)

    if eng_type.lower() == "dfa":
        return list(new_emails)
    elif eng_type.lower() == "re":
        return [new_email[0] for new_email in new_emails]

def initial(): #returns needed DFAs and REs for this project
    ranged_alphas_email = [chr(char) for char in range(ord('a') ,ord('z')+1)] \
            + [chr(char) for char in range(ord('A') ,ord('Z')+1)] \
            + [chr(char) for char in range(ord('0') ,ord('9')+1)]
    ranged_alphas_web = [chr(char) for char in range(ord('a') ,ord('z')+1)] \
            + [chr(char) for char in range(ord('0') ,ord('9')+1)]

    dfa_email = DFA(
            ("q0" ,"q1" ,"q2" ,"q3" ,"q4" ,"q5" ,"qT") 
            ,['.' ,'@' ,'-' ,'_' ,'+'] + ranged_alphas_email
            ,(
                ("q0" ,"q1" ,''.join(ranged_alphas_email + ['.' ,'-' ,'_' ,'+'])), 
                ("q1" ,"q1" ,''.join(ranged_alphas_email + ['.' ,'-' ,'_' ,'+'])), 
                ("q1" ,"q2" ,'@'), 
                ("q2" ,"q3" ,''.join(ranged_alphas_email + ['-'])), 
                ("q2" ,"qT" ,''.join(['@' ,'.' ,'_' ,'+'])), 
                ("q3" ,"q3" ,''.join(ranged_alphas_email + ['-'])), 
                ("q3" ,"q4" ,'.'), 
                ("q3" ,"qT" ,''.join(['@' ,'_' ,'+'])), 
                ("q4" ,"q5" ,''.join(ranged_alphas_email + ['-'])), 
                ("q4" ,"qT" ,''.join(['@' ,'.' ,'_' ,'+'])), 
                ("q5" ,"q5" ,''.join(ranged_alphas_email + ['-'])), 
                ("q5" ,"q4" ,'.'),
                ("q5" ,"qT" ,''.join(['@' ,'_' ,'+']))
            ) 
            ,"q0" 
            ,{"q5"}
            )
    dfa_web = DFA(
            ("q0" ,"q1" ,"q2" ,"q3" ,"q4" ,"q5" ,"q6" ,"q7" ,"q8" ,"q9" ,"q10" ,"q11" ,"q12" ,"q13" ,"q14" ,"q15" ,"qT") 
            ,['!'] + [chr(char) for char in range(ord('#') ,ord('z')+5)]
            ,(
                ("q0" ,"q1" ,'h'), 
                ("q0" ,"q5" ,'w'), 
                ("q1" ,"q2" ,'t'), 
                ("q2" ,"q3" ,'t'),
                ("q3" ,"q4" ,'p'), 
                ("q4" ,"q9" ,':'), 
                ("q4" ,"q15" ,'s'), 
                ("q5" ,"q6" ,'w'), 
                ("q6" ,"q7" ,'w'), 
                ("q7" ,"q8" ,'.'), 
                ("q8" ,"q11" ,''.join(ranged_alphas_web)), 
                ("q9" ,"q10" ,'/'), 
                ("q10" ,"q8" ,'/'), 
                ("q11" ,"q12" ,'.'), 
                ("q11" ,"q11" ,''.join(ranged_alphas_web)), 
                ("q12" ,"q13" ,''.join(ranged_alphas_web)), 
                ("q13" ,"q12" ,'.'), 
                ("q13" ,"q13" ,''.join(ranged_alphas_web)), 
                ("q13" ,"q14" ,'/'), 
                ("q14" ,"q14" ,''.join(['!' ,'#' ,'$' ,'%' ,'&'] + [chr(char) for char in range(ord('(') ,ord('z')+5)])), 
                ("q15" ,"q9" ,':')
                # ("q0" ,"qT" ,'0'), 
                # ("q1" ,"qT" ,''),
                # ("q2" ,"qT" ,'')
            ) 
            ,"q0" 
            ,{"q13" ,"q14"}
            )

    re_email = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]([a-zA-Z0-9-]*(\.[a-zA-Z0-9-])?)*)")
    re_web = re.compile(r"((http[s]?:\/\/|www\.)[a-z0-9]+(\.[a-z]+)+(\/[^\"\'\n]*)?)")

    return (dfa_email ,dfa_web ,re_email ,re_web)

def main(): #driver code
    dfa_email ,dfa_web ,re_email ,re_web = initial()

    while(1):
        clear()
        text = ""

        file_path = input("Please enter Text File Path or Web Address or drag and drop text file here : ")
        if file_path[0] == '&':
            file_path = file_path[3:-1]
        elif  file_path[0] == '\"':
            file_path = file_path[1:-1]
            
        try:
            with open(file_path ,'r') as my_file:
                text = my_file.read()
        except:
            res = get_response(file_path)
            if res:
                text = res.text
            else:
                print("Wrong path")
                continue

        print("File loaded.")

        print("Options :")
        print("1.Use Written DFA to search.")
        print("2.Use default librarys to search.")
        print("3.Reload input file.")
        print("4.Exit.")
        choice = input("Your choice : ")

        if choice == '1':
            print("\nEmails :")
            # print(search(dfa_email ,text))
            for item in search(dfa_email ,text):
                print(item)

            print("\nWeb Addresses :")
            for item in search(dfa_web ,text):
                print(item)

            # print("\nEmails in urls :")
            # print(search_sec_dep(dfa_email ,search(dfa_web ,text)))

        elif choice == '2':
            print("\nEmails :")
            print([email[0] for email in re_email.findall(text)])

            print("\nWeb Addresses :")
            urls = [web[0] for web in re_web.findall(text)]
            print(urls)

            print("\nEmails in urls :")
            print(search_sec_dep(re_email ,urls ,"re"))

        elif choice == '3':
            continue

        elif choice == '4':
            quit()

        else:
            print("Wrong choice.")



if __name__=="__main__":
    main()
