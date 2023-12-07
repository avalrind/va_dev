import re
import os 
import subprocess
import warnings

class v_dev:

    def __init__(self , load_type = 'c++'):
        '''
            Intializizes the object

            Args - 

            1) load_type - Type of path to load (currently only C++ Supported)
        '''

        self.load_type = load_type

        if self.load_type not in [
            'c' , 
            'c++' , 
            'java'
        ] : warnings.warn('Please choose a valid language')

    def convert_to_list(self , val):

        if isinstance(val , list): return val
        else : return [val]

    def re_match(self , value : str , expressions : list) -> list:
        '''
            Searches `expressions` in string and return match object if found. Runs different expressions in a loop

            Args - 

            1) value - String in which the pattern is expected to be found
            2) expressions - List of expressions to look for in `value` 
        '''

        matches = []

        for exp in expressions : 

            for val in value:

                match = re.match(exp , val)

                if match:

                    matches = self.convert_to_list(matches) 
                    
                    matches.append(match.group())

        return matches
    
    def re_find(self , expression : str , value : list) -> list:
        '''
            Return all non-overlapping matches of pattern in string, as a list of strings

            Args - 

            1) value -  String in which the pattern is expected to be found
            2) expressions - List of expressions to look for in `value` 
        '''


        matches = [re.finditer(exp , value , re.MULTILINE|re.DOTALL)
                   for exp 
                   in expression]
        
        r_matches = []

        for f_val in matches:
            for s_val in f_val:
                r_matches.append(s_val.group())

        return set(r_matches)

    
    def load_lib(self, path : str , extra_returns = [] , ignore_main = False , func_regex = [] , class_regex = []):
        '''
            Loads the file into the memory. Search for functions/classes and make seperate Dictionaries to load

            Args - 

            1) path - Absolute Path to the file 
            2) extra_returns - List of extra return types defined in function example `tuple func_name(){\\func_body}`
            3) ignore_main - Ignore the main function or not 
            4) func_regex - Extra regular expression for function
            5) class_regex - Extra regular expression for class
        '''
        
        self.path = path
        self.extra_returns = extra_returns
        self.func_regex = func_regex
        self.class_regex = class_regex


        with open(self.path , 'r') as program: self.content = program.read()

        if self.load_type == 'c++' :
            
            self.lib_patterns = [r'#include\s+[<"]?([^<>"]+)[<"]?>' ,
                                 r'#include \s+[<"]?([^<>"]+)[<"]?>' 
                                 r'# include\s+[<"]?([^<>"]+)[<"]?>' , 
                                 r'# include \s+[<"]?([^<>"]+)[<"]?>']
            self.identifier_pattern = [r'using\s[^;]+;']
            self.func_patterns = [r'int\s+[a-zA-Z_][a-zA-Z_0-9]*\s*\([^)]*\)\s*{[^}]*}' , 
                                  r'void\s+[a-zA-Z_][a-zA-Z_0-9]*\s*\([^)]*\)\s*{[^}]*}'] + self.func_regex
            self.class_patterns = [r'class\s+[a-zA-Z_][a-zA-Z_0-9]*\s*\([^)]*\)\s*{[^}]*}'] + self.class_regex
            
            if self.extra_returns: 
                
                self.ex_funcs = [extra_return + '\s+\w+\s*\([^)]*\)\s*{[^}]*}'
                                 for extra_return
                                 in extra_returns]
                
                self.func_patterns += self.ex_funcs
            
            self.libs = self.re_match(self.content.splitlines() , self.lib_patterns)
            self.s_libs = ''
            for val in self.libs: self.s_libs += val + '\n'
            
            self.identifiers = self.re_find(self.content , self.identifier_pattern)
            self.s_identifiers = ''
            for val in self.identifiers: self.s_identifiers += val + '\n'
            
            self.funcs = self.re_find(self.content , self.func_patterns)
            self.classes = self.re_find(self.content , self.class_patterns)

            self.func_names = [val.split()[1].split('(')[0]
                               for val 
                               in self.funcs]
            self.func_desc = {name : code 
                              for name , code 
                              in zip(self.func_names , self.funcs)}
            
            self.class_names = [val.split()[1].split('(')[0]
                                for val 
                                in self.classes]
            self.class_desc = {name : code 
                               for name , code 
                               in zip(self.class_names , self.classes)}

            if 'main' in self.func_names:
                if ignore_main : pass
                else: 
                    warnings.warn('''The given file has `main()` function. 
                    
                    1) If you want to directly execute the file. Use obj.execute().
                    2) If you want to ignore the main function and still use the file pass `ignore_func = True`''')

                    raise ValueError('File contains main Function')
                
        if self.load_type == 'java' : 

            self.lib_patterns = ['import [a-zA-Z]*' , 
                                 'from [a-zA-Z]* import [a-zA-Z]*']
            
            self.func_patterns = [r'\b(public|private|protected|static|final|\w+)\s+\w+\s+\w+\s*\([^)]*\)\s*\{[^}]*\}']

            self.class_patterns = [r'(class\w+)\s+\w+\s+\w+\s*\([^)]*\)\s*\{[^}]*\}']

            self.libs = self.re_match(self.content.splitlines() , self.lib_patterns)

            self.s_libs = ''
            for val in self.libs : self.s_libs += val + '\n'


            self.funcs = self.re_find(self.func_patterns , self.content )
            self.classes = self.re_find(self.class_patterns , self.content)


            self.func_names = [val.split()[2].split('(')[0]
                               for val 
                               in self.funcs]
            self.func_desc = {name : code 
                              for name , code 
                              in zip(self.func_names , self.funcs)}
            
            print(self.func_desc)

            self.class_names = [val.split()[1].split('(')[0]
                                for val 
                                in self.classes]
            self.class_desc = {name : code
                               for name , code 
                               in zip(self.class_names , self.classes)}
            
            if 'main' in self.func_names: 

                if ignore_main : pass 
                else : 
                    warnings.warn('''The given file has `main()` function. 
                    
                    1) If you want to directly execute the file. Use obj.execute().
                    2) If you want to ignore the main function and still use the file pass `ignore_func = True`''')

                    raise ValueError('File contains main Function')


    def arg_builder(self , args : list):
        '''
            Builds Arguments to be passed to the function selected 

            Args - 
            1) args - List of arguments 
        '''

        counter = 0
        arguments = ''
        for val in args : 
            if counter == len(args) - 1: arguments += str(val)
            else : 
                arguments += str(val) + str(',')
                counter += 1

        return arguments 

    def execute(self , file_name : str):

        if self.load_type == 'c++':

            os.system(f'g++ {file_name}')

            try : r = subprocess.run([f'{self.func_name}.exe'])
            except Exception as e : r = subprocess.run(['a.exe'])

            return r
        
        elif self.load_type == 'java': 

            os.system(f'javac {file_name}.java')

            r = subprocess.run(['java' , f'{self.func_class_name}'])

            return r

    def load_func(self , func_name : str , args = [] , multiple_returns = False , multiple_args = None , func_class_name = 'Jav'):
        '''
            Loads the function into existance. Creates the function files and Run them as per the arguments

            Args - 
            1) func_name - Name of the function to be loaded
            2) args - List of arguments to be passed in 
            3) multiple_returns - If the function returns multiple values. Set this to True
        '''
        self.func_class_name = func_class_name
        self.func_name = func_name
        self.args = args
        self.multiple_returns = multiple_returns
        self.multiple_args = multiple_args

        if self.args == []:warnings.warn('''args is passed empty. 
                                         This can lead to not making of the exe file if the function requires arguments. 
                                         If the function do not require arguments Please ignore this warning''')

        if self.load_type == 'c++':

            self.multiple_args_line = ''

            if self.multiple_returns :
                self.s_libs += '\n#include <fstream>' 
                self.write_func = '''
void WriteResultToFile(const vector<int>& data) {
    ofstream outputFile("output.txt");
    if (outputFile.is_open()) {
        for (int value : data) {outputFile << value << " ";}
        outputFile.close();}
    else {cerr << "Error: Unable to open the output file." << endl;}}'''
                
                self.main_func = 'int main(){\n\t' + f'{self.multiple_args} result = {func_name}({self.arg_builder(self.args)});\n' +f'\t WriteResultToFile(result);\n' + '\t return 0;\n}'
                self.write_up = f'{self.s_libs}\n{self.s_identifiers}\n{self.func_desc[self.func_name]}\n{self.write_func}\n{self.main_func}'
            
            else : 
                self.main_func = 'int main(){\n\t' + f'{func_name}({self.arg_builder(self.args)});\n' + '\t return 0;\n}'
                self.write_up = f'{self.s_libs}\n{self.s_identifiers}\n{self.func_desc[self.func_name]}\n{self.main_func}' 
        
            with open (f'{self.func_name}.cpp' , 'w') as func_program: func_program.write(self.write_up)

            return_val = self.execute(file_name = f'{self.func_name}.cpp')

            if self.multiple_args:
                with open('output.txt' , 'r') as output : return_s = output.read()

                return_val = return_s.split()

            return return_val

        elif self.load_type == 'java' : 

            self.write_up = f'public class {self.func_class_name}' + '{\n\n\t' + f'{self.func_desc[self.func_name]}' + '\n\t' + '\n\tpublic static void main(String[] args){\n\t' + f'{self.func_name}({self.arg_builder(self.args)});' + '}\n\t' + '}'

            with open(f'{self.func_class_name}.java' , 'w') as func_program : func_program.write(self.write_up)

            return_val = self.execute(file_name = f'{self.func_name}.java')

            return return_val
        
    def load_class(self , class_name , obj_name = 'sample_object' , args = []) : 
        '''
            Loads the class into existance. Creates the class/object files and Run them as per the arguments

            Args - 
            1) class_name - Name of the class to be loaded
            2) obj_name - Name of the object to be created to the class
            3) args - List of arguments to be passed in 
        '''
        
        self.class_name = class_name
        self.obj_name = obj_name 
        self.args = args

        if self.load_type == 'c++':

            self.main_func = 'int main(){\n\t' + f'{self.class_name} {self.obj_name}({self.arg_builder(self.args)});\n' + '\t return 0;\n}'
            self.write_up = self.s_libs + '\n' + self.class_desc[self.class_name] + '\n' + self.main_func

            with open(f'{self.class_name}.cpp' , 'w') as class_pogram: class_pogram.write(self.write_up)

            return_val = self.execute(file_name = f'{self.class_name}.cpp')

            return return_val
