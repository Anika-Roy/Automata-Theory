# Programming Assignment
Automata Theory Monsoon 2023, IIIT Hyderabad

**General Instructions:** This programming assignment focuses on two challenging tasks related to automata theory and compiler design. The purpose of this assignment is not just to test your coding skills but also to evaluate your understanding of fundamental concepts. It's important to note that there will be an evaluation/viva after the submission, which will contribute to a part of your grade.

**Language Constraints:** You are required to implement your solutions in Python. Additionally, your code should handle input/output from both files and standard output (stdout). If you intend to use any libraries beyond the standard Python libraries, please consult with one of the Teaching Assistants for approval. Any submissions in languages other than Python will not be evaluated.

## 1 Probabilistic Auto-complete
**Task Overview:** In this part of the assignment, you will create an auto-complete system using a Probabilistic Finite-State Automaton (PFSA) based on a given text corpus. The PFSA will operate at the letter-level, providing auto-complete suggestions for words based on the input prefix.

### Rules and Requirements:
#### 1.1 Rules on PFSA
**1.1.1 States:** Each state in your PFSA represents a sequence of letters. It's crucial to ensure that the PFSA does not contain any dead states. A dead state is a state whose incoming probability is zero. To distinguish between a prefix and a valid English word in your PFSA, mark words from the text corpus with an asterisk (*) at the end.

**1.1.2 Transitions:** The transitions in your PFSA should be positively weighted and directed. According to probability axioms, the sum of outgoing probabilities from each state must add up to one. The incoming probabilities do not necessarily need to add up to one.

**1.1.3 Initial State:** The initial state is represented using an asterisk (*). It should have edges to nodes with only one letter, and the weights of these edges should be based on the text corpus.

**1.1.4 End States:** States representing valid English words from the corpus are considered end states. These end states should be marked appropriately.

### Example:
Let's assume that the text corpus contains only three words: Auto, Automata, and Automate. Your PFSA will include all the prefixes of these words with transition probabilities.

### Input/Output Format:
You will receive a boilerplate for handling most of the input/output operations. Ensure that your output PFSA is stored in JSON format, adhering to the specified structure.

### Sampling from PFSA:
After constructing the PFSA, you will create a program that generates random words based on the PFSA. The program should be capable of taking a PFSA stored in a JSON file and producing random words following the distribution.

### Validation:
The validity of your PFSA file will be assessed by calculating the frequencies of each word and ensuring that it closely matches the expected distribution.

### Submission Details:
A dedicated portal for Question 1 will be provided for submission. You should submit a zip file containing two Python programs: `pfsa.py` for the PFSA construction (Part I) and `generator.py` for word generation (Part II). The zip file should be named `roll_number_AT1.zip`.

## 2 Compiler with Tokenization and CFG Parsing
**Task Overview:** In this part of the assignment, you will build a compiler for a simple programming language that supports various token types, including identifiers, keywords, integers, floating-point numbers, and symbols. The goal is to implement tokenization (lexical analysis) and syntactic analysis using a given context-free grammar (CFG).

### Detailed Requirements:
#### 2.1 Rules for Syntactic Analysis
You are expected to implement the following rules for syntactic analysis based on the provided CFG:
1. S → statement
2. statement → if (A)| (statement)(statement) | y
3. y ∈ statement alphabets [Σstatement]
4. A → (cond)(statement) | (cond)(statement)(else)(statement)
5. cond → (x)(op1)(x) | x
6. op1 → + | - | * | / |ˆ| < | > | =
7. x → R | cond | y

#### 2.3 Input/Output Format:
When the program is executed, it should prompt the user for an input statement.

**2.3.1 Input:**
The input is a single line of text representing a program statement.

**2.3.2 Output:**
1. If there are no errors (neither syntactical nor lexical), the program should output each token's type and value on separate lines.
2. If a lexical error is detected (e.g., an invalid identifier), raise an error with a brief description.
3. If a syntactic error is detected (e.g., the code doesn't follow the provided grammar), raise an error with an informative description.

### Sample Test Cases:
Here are some sample inputs and expected outputs to help you understand the expected behavior of your compiler.

### Assumptions made
1. The set of symbols = set of operators
2. ; is not handled in the grammar (No statement should end with them either)
3. Negative numbers aren't handled in the grammar either

### References and discussions:
1. The code for CYK algorithm was obtained from ChatGPT and pseudocode from https://courses.engr.illinois.edu/cs373/sp2009/lectures/lect_15.pdf
2. I have discussed my approach and error-handling techniques with my peers

### Error Handling List:

1. Check if else's are more than if's
2. Check if the first else comes before the first if
3. Can't start with an operator or an else
4. Two operators can't be adjacent to each other
5. A statement cannot end with an "else" (or) an operator
6. There must be at least 2 arguments after if: second last position can also not be if
7. Only an if or an operator can come 2 positions before an operator
8. The minimum distance between an else and an operator must be greater than or equal to 2
