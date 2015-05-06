import lxml.html
import sys

def convertToBoostRepos(input_string):
    # some libraries need to be renamed
    if( input_string == "numeric~odeint" ):
        return "odeint"
    if( input_string == "numeric~conversion" ):
        return "conversion"
    if( input_string == "numeric~ublas" ):
        return "ublas"
    if( input_string == "numeric~interval" ):
        return "interval"
    # some strings are not libraries
    garbage_strings = [u'\u21e2', u'(unknown)']
    if( input_string in garbage_strings ):
        return ""
    return input_string

def convert_raw_dependencies_string_to_list(deps_str):
    if( deps_str is None ):
        return []
    raw_list = deps_str.split()
    good_list = []
    for el in raw_list:
        good_el = convertToBoostRepos(el)
        if( good_el != "" ):
            good_list.append(good_el)
    return good_list 
  
def generate_boost_dependency_file(input_boostdep_filename, output_cmake_filename):
    
    # dictionary of all library (keys) and their dependecies (values saved as list)
    libs = {};
    
    root = lxml.html.fromstring(open(input_boostdep_filename).read())
    
    # h2 elements contains libraries, while the p contain the dependencies
    h2s = root.cssselect("h2")
    paragraphs = root.cssselect("p")
    
    del paragraphs[-1]
    
    assert(len(h2s) == len(paragraphs))
    
    for i in range(0,len(h2s)):
        libs[convertToBoostRepos(h2s[i][0][0].text)] = set(convert_raw_dependencies_string_to_list(paragraphs[i][0].text))
        
    # expand dependencies 
    # 20 is magic number to ensure that we repeat the process enough
    for i in range(0,20):
        print("Expanding dependencies, cycle " + unicode(i))
        for lib in libs:
            print("Expanding library lib" + lib)
            print("with deps ")
            print(libs[lib])
            deps = list(libs[lib])
            for dep in deps:
                libs[lib] = libs[lib].union(libs[dep])
        # remove duplicates
         
    
    # generate cmake boost dependency file
    cmake_file = open(output_cmake_filename,'w')
    
    cmake_file.write("# File automatically generated by the generateBoostDependencies.py script from boostdep output\n")
    cmake_file.write("\n\n\n");
    
    for lib in libs:
        
        set_string = 'set('+lib+'_BOOST_COMPONENTS_DEPENDS '
        
        cmake_file.write(set_string)
        deps = list(libs[lib])
        for dep_i in range(0,len(deps)):
            dep = deps[dep_i];
            #indent 
            if( dep_i != 0 ):
                cmake_file.write(" "*len(set_string))
                
            
            cmake_file.write("\"" + dep + "\"");
            
            #add new line
            if( dep_i != len(libs[lib])-1 ):
                cmake_file.write("\n")
        cmake_file.write(')\n\n')
    
    cmake_file.close()
    
def print_help():
    print("Usage: generateBoostDependencies.py module-overview.html")

def main():
    if( len(sys.argv) != 2 or sys.argv[1] == "--help" ):
        print_help()
    else:
        generate_boost_dependency_file(sys.argv[1],"BoostDependencies.cmake")
        
if __name__ == "__main__":
    main()

