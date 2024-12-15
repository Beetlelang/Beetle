import re
import math

# Define keywords that should not be executed immediately
keywords = ["if", "for", "while", "else", "guard", "async", "await", "try", "catch", "finally", "lambda"]

# Dictionary to store variables with explicit types
variables = {}

# Global variable for tracking line numbers
line = 1

# Function to handle variable typing and coercion
def cast_value(value, to_type):
    """Explicit casting with weak typing control."""
    try:
        if to_type == "int":
            return int(value)
        elif to_type == "float":
            return float(value)
        elif to_type == "str":
            return str(value)
        elif to_type == "bool":
            return bool(value)
        else:
            raise ValueError("Unsupported type conversion")
    except ValueError:
        print(f"Error: Cannot cast {value} to {to_type}")
        return None

# Function to execute Langbeet code
def langbeet_compile(code, code_block=None):
    global line  # Make line a global variable

    try:
        # Handle println() function (output)
        if 'println' in code:
            match = re.match(r"println\((.*)\)", code)
            if match:
                content = match.group(1).strip()
                if content.startswith("f\"") and content.endswith("\""):
                    print(content[2:-1])  # Handle f-string
                elif content.startswith("\"") and content.endswith("\""):
                    print(content[1:-1])  # Regular string
                elif content in variables:
                    print(variables[content])  # Print stored variable
                else:
                    print(content)

        # Handle mathematical functions and operations
        elif 'sqrt' in code:
            match = re.match(r"sqrt\((.*)\)", code)
            if match:
                value = float(match.group(1).strip())
                print(math.sqrt(value))
        
        # Handle exponentiation (x ** y)
        elif '**' in code:
            operands = re.findall(r"(\d+\.?\d*)\s*\*\*\s*(\d+\.?\d*)", code)
            if operands:
                base, exponent = map(float, operands[0])
                print(base ** exponent)
        
        # Handle addition (+)
        elif '+' in code:
            operands = re.findall(r"(\d+\.?\d*)\s*\+\s*(\d+\.?\d*)", code)
            if operands:
                left, right = map(float, operands[0])
                print(left + right)
        
        # Handle subtraction (-)
        elif '-' in code:
            operands = re.findall(r"(\d+\.?\d*)\s*\-\s*(\d+\.?\d*)", code)
            if operands:
                left, right = map(float, operands[0])
                print(left - right)
        
        # Handle division (/)
        elif '/' in code:
            operands = re.findall(r"(\d+\.?\d*)\s*/\s*(\d+\.?\d*)", code)
            if operands:
                left, right = map(float, operands[0])
                if right == 0:
                    print("inf")
                else:
                    print(left / right)
        
        # Handle variable assignment with strong typing
        elif '=' in code:
            match = re.match(r"(\w+)\s*=\s*(.*)", code)
            if match:
                var_name = match.group(1)
                value = match.group(2).strip()

                # Check if value is an explicit type conversion (e.g., cast to int, float, etc.)
                if re.match(r"int\((.*)\)", value):
                    content = re.match(r"int\((.*)\)", value).group(1).strip()
                    variables[var_name] = cast_value(content, "int")
                elif re.match(r"float\((.*)\)", value):
                    content = re.match(r"float\((.*)\)", value).group(1).strip()
                    variables[var_name] = cast_value(content, "float")
                elif re.match(r"str\((.*)\)", value):
                    content = re.match(r"str\((.*)\)", value).group(1).strip()
                    variables[var_name] = cast_value(content, "str")
                elif re.match(r"bool\((.*)\)", value):
                    content = re.match(r"bool\((.*)\)", value).group(1).strip()
                    variables[var_name] = cast_value(content, "bool")
                else:
                    # Handle as a regular assignment
                    if value in variables:
                        variables[var_name] = variables[value]
                    elif value.isdigit() or re.match(r"\d+\.\d+", value):  # Check for numeric values
                        variables[var_name] = float(value) if '.' in value else int(value)
                    else:
                        variables[var_name] = value  # Store the raw value as a string
                print(f"Variable {var_name} set to {variables[var_name]}")
        
        # Handle for loop specifically (optimized for performance)
        elif 'for' in code:
            if code_block is None:
                code_block = "for_loop"
            if 'range' in code:
                start, end = map(int, re.findall(r'\d+', code))
                batch_size = 1000  # Print in batches
                output = []
                for i in range(start, end + 1):
                    output.append(str(i))
                    if len(output) >= batch_size:
                        print(" ".join(output))
                        output = []
                if output:
                    print(" ".join(output))
            return code_block

        # Handle lambda expressions
        elif 'lambda' in code:
            match = re.match(r"lambda\s+(\w+)\s*:\s*(.*)", code)
            if match:
                var_name = match.group(1)
                expr = match.group(2)
                # Store lambda functions as strings or create a callable mechanism
                print(f"Lambda function: {var_name} -> {expr}")
        
        # Handle async/await
        elif 'async' in code or 'await' in code:
            print(f"Async operation or await detected in: {code}")
        
        # Guard clauses (early return)
        elif 'guard' in code:
            match = re.match(r"guard\s+([^\s]+)\s+then\s+([^\s]+)", code)
            if match:
                condition = match.group(1)
                action = match.group(2)
                print(f"Guard clause: {condition} then {action}")
        
        # Handle try/catch/finally
        elif 'try' in code or 'catch' in code or 'finally' in code:
            print(f"Error handling block detected: {code}")
        
        else:
            print(f"Unsupported code on line {line}: {code}")
            line += 1
        
    except Exception as e:
        print(f"Error on line {line}: {code}\n{e}")
        line += 1

# Main function to control the flow of the compiler
def run_langbeet_compiler():
    global line
    print("Langbeet Compiler - Type your code!")
    print("Use >> to continue after a keyword is detected.")
    
    code_input = ">>"
    code_block = None

    while True:
        # Get the code input from the user
        code_input = input(code_input + "\n").strip()

        if code_input == 'exit':
            break  # Exit the compiler loop
        
        if code_input == '>>':
            continue  # Continue if the user types '>>'
        
        # Handle special keywords
        if any(keyword in code_input for keyword in keywords):
            print(f"Keyword detected, please continue with '>>'")
            code_block = langbeet_compile(code_input, code_block)  # Handle the block input
        else:
            langbeet_compile(code_input, code_block)  # Compile the regular line

        # After processing, show the >> prompt again
        code_input = ">>"
        line += 0  # Increment line after processing each code

# Start the Langbeet compiler
run_langbeet_compiler()
