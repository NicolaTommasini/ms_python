import math

def shunting_yard(expression,x):
    expression = expression.replace('x', str(x))
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3, 'sin': 3, 'cos': 3, 'tan': 3, 'cot': 3}

    def apply_operator(operator, operand_stack):
        if operator == '+':
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            result = operand1 + operand2
            operand_stack.append(result)
        elif operator == '-':
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            result = operand1 - operand2
            operand_stack.append(result)
        elif operator == '*':
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            result = operand1 * operand2
            operand_stack.append(result)
        elif operator == '/':
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            result = operand1 / operand2
            operand_stack.append(result)
        elif operator == '%':
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            result = operand1 % operand2
            operand_stack.append(result)
        elif operator == '^':
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            result = operand1 ** operand2
            operand_stack.append(result)
        elif operator == 'sin':
            operand = operand_stack.pop()
            result = math.sin(operand)
            operand_stack.append(result)
        elif operator == 'cos':
            operand = operand_stack.pop()
            result = math.cos(operand)
            operand_stack.append(result)
        elif operator == 'tan':
            operand = operand_stack.pop()
            result = math.tan(operand)
            operand_stack.append(result)
        elif operator == 'cot':
            operand = operand_stack.pop()
            result = 1 / math.tan(operand)
            operand_stack.append(result)

    def evaluate_expression(tokens):
        operator_stack = []
        operand_stack = []

        for token in tokens:
            if token.replace('.', '', 1).isdigit():  # Check if token is a float
                operand_stack.append(float(token))
            elif token.isalpha():
                operator_stack.append(token)
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       precedence[token] <= precedence[operator_stack[-1]]):
                    apply_operator(operator_stack.pop(), operand_stack)
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack[-1] != '(':
                    apply_operator(operator_stack.pop(), operand_stack)
                operator_stack.pop()  # Pop the '('

        while operator_stack:
            apply_operator(operator_stack.pop(), operand_stack)

        return operand_stack[0]

    def tokenize(expression):
        tokens = []
        i = 0

        while i < len(expression):
            if expression[i].isdigit() or expression[i] == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                tokens.append(expression[i:j])
                i = j
            elif expression[i].isalpha():
                func_name = ""
                while i < len(expression) and expression[i].isalpha():
                    func_name += expression[i]
                    i += 1
                tokens.append(func_name)
            else:
                tokens.append(expression[i])
                i += 1

        return tokens

    # Tokenize the expression
    tokens = tokenize(expression)

    # Evaluate the expression
    result = evaluate_expression(tokens)

    return result

import argparse
import re


def parse_values(values_str):
    values = re.split(r'\s*,\s*', values_str)
    values = [float(x) for x in values]
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
        result = shunting_yard(expression, x)
        results.append(result)
    print(*results, sep=', ')

if __name__ == '__main__':
    main()
