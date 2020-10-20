import random
import subprocess

base = """
#include <functional>
struct Foo {
  Foo() {};
  auto operator()() {
    return Foo();
  };
  auto operator()(int) {
    return Foo();
  };
  auto operator()(Foo) {
    return Foo();
  };
  auto operator()(std::function <void (int)>) {
    return Foo();
  };
  auto operator[](int) {
    return Foo();
  };
  auto operator[](Foo) {
    return Foo();
  };
  auto operator[](std::function <void (int)>) {
    return Foo();
  };
};
"""

tokens = [
        "[",
        "]",
        "{",
        "}",
        "(",
        ")",
        "0",
        ";",
        "Foo",
        ]

def expression_generator(max_len):
    # randomly combine tokens in to a string of up to length max_len
    # while True:
    already_generated_expressions = []
    for i in range(1000000):
        generated_expression = ""
        for j in range(max_len):
            token = random.choice(tokens)
            generated_expression += token
        if generated_expression not in already_generated_expressions:
            yield generated_expression
        already_generated_expressions.append(generated_expression)

for max_len in range(1,10):
    for generated_expression in expression_generator(max_len):
        generated_code_str = base + f"int main() {{ {generated_expression}; }}"
        filename = '.tmp.cpp'
        outfile = '.tmp'
        with open(filename, 'w') as f:
            f.write(generated_code_str)

        args = ["g++", "-w", "-I.", "-fpermissive", '-O0', filename, '-o', outfile]
        result = subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            print(f"{generated_expression}")

