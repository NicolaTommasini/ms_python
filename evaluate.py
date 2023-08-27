import argparse
from typing import List

import math
import re
OPERATORS = {'+': 1, '-': 1, '*': 2, '/': 2}
FUNCTIONS = {'cos', 'sin', 'tan', 'sqrt','log'}

def check_brackets(expression):
    stack = []
    for char in expression:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0
def replace_operators(expression):
    expression = expression.replace('^', '**')
    return expression
def tokenize(expression):
    pattern = r"(\w+|\d+\.\d+|\d+|[()+\-*\/])"
    tokens = re.findall(pattern, expression)
    return tokens
def evaluate(tokens):
    output_queue = []
    operator_stack = []
    for token in tokens:
        if token.replace('.', '').isdigit():
            output_queue.append(float(token))
        elif token in FUNCTIONS:
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()
            if operator_stack and operator_stack[-1] in FUNCTIONS:
                function = operator_stack.pop()
                argument = output_queue.pop()
                output_queue.append(apply_function(function, argument))
        elif token in OPERATORS:
            while operator_stack and operator_stack[-1] in OPERATORS and has_precedence(operator_stack[-1], token):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
    while operator_stack:
        output_queue.append(operator_stack.pop())
    result = evaluate_postfix(output_queue)
    return result
def apply_function(function, argument):
    if function == 'cos':
        return math.cos(argument)
    elif function == 'sin':
        return math.sin(argument)
    elif function == 'tan':
        return math.tan(argument)
    elif function == 'sqrt':
        return math.sqrt(argument)
    elif function == 'log':
        return math.log(argument)
    else:
        raise ValueError("Unsupported function: " + function)
def has_precedence(operator1, operator2):
    return OPERATORS[operator1] >= OPERATORS[operator2]
def evaluate_postfix(tokens):
    stack = []
    for token in tokens:
        if isinstance(token, float):
            stack.append(token)
        elif token in OPERATORS:
            operand2 = stack.pop()
            operand1 = stack.pop()
            result = apply_operation(token, operand1, operand2)
            stack.append(result)
    return stack[0]
def apply_operation(operator, operand1, operand2):
    if operator == '+':
        return operand1 + operand2
    elif operator == '-':
        return operand1 - operand2
    elif operator == '*':
        return operand1 * operand2
    elif operator == '/':
        return operand1 / operand2
    else:
        raise ValueError("Unsupported operator: " + operator)
    
def evaluate_expression(expression,x):
    expression = expression.replace('x', str(x))
    expression = expression.replace(' ', '')  # Remove whitespace from the expression
    if not check_brackets(expression):
        return "Invalid expression: Brackets are not balanced"
    expression = replace_operators(expression)
    tokens = tokenize(expression)
    return evaluate(tokens)


import argparse
def parse_values(values_str):
    values = re.split(r'\s*,\s*', values_str)
    values = [int(x) for x in values]
    return values

def parse_arguments():
    parser = argparse.ArgumentParser(description='Expression Evaluator')
    parser.add_argument('--expression', required=True, help='Expression to evaluate')
    parser.add_argument('--at', required=True, help='Values of x separated by commas')
    args = parser.parse_args()
    expression = args.expression
    values = parse_values(args.at)
    return expression, values

def main():
    expression, values = parse_arguments()
    results = []
    for x in values:
        result = evaluate_expression(expression, x)
        results.append(result)
        # print all the result separted by comma the last one without comma
    print(*results,sep=', ')

if __name__ == '__main__':
    main()