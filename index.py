class CoreFunctions:
    @staticmethod
    def remove_leading_whitespace(text):
        """
        Remove leading spaces and tabs from the given text.

        Args:
            text (str): The input text.

        Returns:
            str: The text with leading whitespace removed.
        """
        index = 0
        while text[index] == ' ' or text[index] == '\t':
            index += 1
        return text[index:]
    
    @staticmethod
    def remove_trailing_whitespace(text):
        """
        Remove trailing spaces, newlines, and tabs from the given text.

        Args:
            text (str): The input text.

        Returns:
            str: The text with trailing whitespace removed.
        """
        index = 1
        while index <= len(text) and (text[-index] == ' ' or text[-index] == '\n' or text[-index] == '\t'):
            index += 1
        return text[:(len(text) + 1) - index]

    @staticmethod
    def remove_whitespace(text):
        """
        Remove both leading and trailing spaces, newlines, and tabs from the given text.

        Args:
            text (str): The input text.

        Returns:
            str: The text with leading and trailing whitespace removed.
        """
        return CoreFunctions.remove_trailing_whitespace(CoreFunctions.remove_leading_whitespace(text))

    @staticmethod
    def append_to_list(lst, item):
        """
        Append an item to the list.

        Args:
            lst (list): The list to append to.
            item (Any): The item to append.

        Returns:
            list: The list with the appended item.
        """
        lst += [item]
        return lst

    @staticmethod
    def convert_to_integer(text):
        """
        Convert a string to an integer. Returns False if the string is not a valid integer.

        Args:
            text (str): The string to convert.

        Returns:
            int: The converted integer or False if conversion is not possible.
        """
        result = 0
        for char in text:
            if char == ' ':
                return False
            if char == '#':
                continue
            if char == '.':
                raise ValueError("Input file has an invalid format")
            if ord(char) < ord('0') or ord(char) > ord('9') + 1:
                return False
            result = (result * 10) + (ord(char) - ord('0'))
        if text[0] == '#':
            result *= -1
        return result

    @staticmethod
    def merge_arrays(arr, left, mid, right):
        """
        Merge two halves of an array for merge sort.

        Args:
            arr (list): The array to be merged.
            left (int): The left index.
            mid (int): The middle index.
            right (int): The right index.
        """

        sub_arr_one_size = mid - left + 1
        sub_arr_two_size = right - mid

        left_arr = [0] * sub_arr_one_size
        right_arr = [0] * sub_arr_two_size

        for i in range(sub_arr_one_size):
            left_arr[i] = arr[left + i]
        for j in range(sub_arr_two_size):
            right_arr[j] = arr[mid + 1 + j]

        left_index = 0  
        right_index = 0  
        merged_index = left 

        while left_index < sub_arr_one_size and right_index < sub_arr_two_size:
            if left_arr[left_index] <= right_arr[right_index]:
                arr[merged_index] = left_arr[left_index]
                left_index += 1
            else:
                arr[merged_index] = right_arr[right_index]
                right_index += 1
            merged_index += 1

        while left_index < sub_arr_one_size:
            arr[merged_index] = left_arr[left_index]
            left_index += 1
            merged_index += 1

        while right_index < sub_arr_two_size:
            arr[merged_index] = right_arr[right_index]
            right_index += 1
            merged_index += 1

    @staticmethod
    def merge_sort(arr, start, end):
        """
        Sort the array using the merge sort algorithm.

        Args:
            arr (list): The array to be sorted.
            start (int): The beginning index.
            end (int): The ending index.
        """

        if start >= end:
            return

        mid = start + (end - start) // 2
        CoreFunctions.merge_sort(arr, start, mid)
        CoreFunctions.merge_sort(arr, mid + 1, end)
        CoreFunctions.merge_arrays(arr, start, mid, end)


class SparseMatrix:
    "Blueprint for sparse matrices."
    def __init__(self, rows, cols):
        """
        Initialize a sparse matrix with given rows and columns.

        Args:
            rows (int): The number of rows in the matrix.
            cols (int): The number of columns in the matrix.
        """
        self.rows = rows
        self.cols = cols
        self.data = []

    def insert_value(self, row, col, value):
        """
        Insert a value into the matrix at the specified row and column.

        Args:
            row (int): The row index.
            col (int): The column index.
            value (int): The value to insert.

        Raises:
            ValueError: If the position is invalid.
        """
        if row >= self.rows or col >= self.cols:
            raise ValueError("Invalid matrix position")
        if value != 0:
            CoreFunctions.append_to_list(self.data, [row, col, value])

    def add_matrices(self, other):
        """
        Add two sparse matrices.

        Args:
            other (SparseMatrix): The matrix to add.

        Returns:
            SparseMatrix: The resulting matrix after addition.

        Raises:
            ValueError: If the dimensions do not match.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match")

        result = SparseMatrix(self.rows, self.cols)
        CoreFunctions.merge_sort(self.data, 0, len(self.data) - 1)
        CoreFunctions.merge_sort(other.data, 0, len(other.data) - 1)

        self_pos = other_pos = 0
        while self_pos < len(self.data) and other_pos < len(other.data):
            self_row, self_col, self_val = self.data[self_pos]
            other_row, other_col, other_val = other.data[other_pos]

            if (self_row < other_row) or (self_row == other_row and self_col < other_col):
                CoreFunctions.append_to_list(result.data, [self_row, self_col, self_val])
                self_pos += 1
            elif (other_row < self_row) or (other_row == self_row and other_col < self_col):
                CoreFunctions.append_to_list(result.data, [other_row, other_col, other_val])
                other_pos += 1
            else:
                if self_val + other_val != 0:
                    CoreFunctions.append_to_list(result.data, [self_row, self_col, self_val + other_val])
                self_pos += 1
                other_pos += 1

        while self_pos < len(self.data):
            CoreFunctions.append_to_list(result.data, self.data[self_pos])
            self_pos += 1

        while other_pos < len(other.data):
            CoreFunctions.append_to_list(result.data, other.data[other_pos])
            other_pos += 1
        return result
    
    def subtract_matrices(self, other):
        """
        Subtract two sparse matrices.

        Args:
            other (SparseMatrix): The matrix to subtract.

        Returns:
            SparseMatrix: The resulting matrix after subtraction.

        Raises:
            ValueError: If the dimensions do not match.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match")

        result = SparseMatrix(self.rows, self.cols)
        CoreFunctions.merge_sort(self.data, 0, len(self.data) - 1)
        CoreFunctions.merge_sort(other.data, 0, len(other.data) - 1)

        self_pos = other_pos = 0
        while self_pos < len(self.data) and other_pos < len(other.data):
            self_row, self_col, self_val = self.data[self_pos]
            other_row, other_col, other_val = other.data[other_pos]

            if (self_row < other_row) or (self_row == other_row and self_col < other_col):
                CoreFunctions.append_to_list(result.data, [self_row, self_col, self_val])
                self_pos += 1
            elif (other_row < self_row) or (other_row == other_row and other_col < self_col):
                CoreFunctions.append_to_list(result.data, [other_row, other_col, -other_val])
                other_pos += 1
            else:
                if self_val - other_val != 0:
                    CoreFunctions.append_to_list(result.data, [self_row, self_col, self_val - other_val])
                self_pos += 1
                other_pos += 1

        while self_pos < len(self.data):
            CoreFunctions.append_to_list(result.data, self.data[self_pos])
            self_pos += 1

        while other_pos < len(other.data):
            CoreFunctions.append_to_list(result.data, [other.data[other_pos][0], other.data[other_pos][1], -other.data[other_pos][2]])
            other_pos += 1

        return result

    def transpose_matrix(self):
        """
        Transposes a matrix by switching its columns with its rows.
        Returns:
            SparseMatrix: The resulting matrix after transposing.
        """

        result = SparseMatrix(self.cols, self.rows)
        for row, col, val in self.data:
            result.insert_value(col, row, val)
        return result

    def multiply_matrices(self, other):
        """
        Multiply two sparse matrices.

        Args:
            other (SparseMatrix): The matrix to multiply with.

        Returns:
            SparseMatrix: The resulting matrix after multiplication.

        Raises:
            ValueError: If the dimensions do not allow multiplication.
        """
        if self.cols != other.rows:
            raise ValueError("Invalid matrix dimensions for multiplication")

        result = SparseMatrix(self.rows, other.cols)
        other_transposed = other.transpose_matrix()

        non_zero_elements = {}
        for self_row, self_col, self_val in self.data:
            for other_row, other_col, other_val in other.data:
                if self_col == other_row:
                    if (self_row, other_col) not in non_zero_elements:
                        non_zero_elements[(self_row, other_col)] = 0
                    non_zero_elements[(self_row, other_col)] += self_val * other_val
        for (row, col), val in non_zero_elements.items():
            if val != 0:
                result.insert_value(row, col, val)

        return result

    def print_matrix(self):
        """
        Print the sparse matrix.

        Prints the dimensions and all non-zero elements in row-column-value format.
        """

        print(f"Dimension: {self.rows} x {self.cols}")
        print("Sparse Matrix: Row Column Value")
        for row, col, val in sorted(self.data):
            print(row, col, val)


def extract_parts(text):
    """
    Extract parts of a string within parentheses, separated by commas in the format of (row, column, value).

    Args:
        text (str): The input string.

    Returns:
        list: A list of parts extracted from the string.
    """
    output = []
    if text[0] == '(':
        part = ''
        for char in text[1:]:
            if char != ' ' and char != ',' and char != ')':
                part += char
            elif char == ',' or char == ')':
                CoreFunctions.append_to_list(output, part)
                part = ''
    return output

def split_string(text, split_char):
    """
    Split a string by a specified character.

    Args:
        text (str): The input string.
        split_char (str): The character to split by.

    Returns:
        list: A list of parts after splitting.
    """
    output = []
    part = ''
    for char in text:
        if char != split_char:
            part += char
        else:
            CoreFunctions.append_to_list(output, part)
            part = ''
    CoreFunctions.append_to_list(output, part)
    return output

# Stores dimensions of the matrix.
dimensions = {}

def process_input_file(input_path):
    """
    Process the input file and create a sparse matrix.

    Args:
        input_path (str): The path to the input file.

    Returns:
        SparseMatrix: The created sparse matrix.
    """
    with open(input_path, 'r') as file:
        skipped_lines = 0
        split_line = split_string(file.readline(), '=')
        dimensions[split_line[0]] = split_line[-1]
        split_line = split_string(file.readline(), '=')
        dimensions[split_line[0]] = split_line[-1]
        rows = CoreFunctions.convert_to_integer(dimensions['rows'].strip())
        cols = CoreFunctions.convert_to_integer(dimensions['cols'].strip())
        matrix = SparseMatrix(rows, cols)
        for line in file:
            try:
                line = line.strip()
                if line == '':
                    continue
                row_num, col_num, value = [CoreFunctions.convert_to_integer(part.strip()) for part in extract_parts(line)]
            except:
                print(extract_parts(line))
                raise ValueError("Input file has an invalid format")
            try:
                matrix.insert_value(row_num, col_num, value)
            except Exception:
                skipped_lines += 1
                continue
        return matrix
    
def output_results(output_path, results, rows, cols):
    """
    Output the results to a file.

    Args:
        output_path (str): The path to the output file.
        results (list): The list of results to write.
        rows (int): The number of rows.
        cols (int): The number of columns.
    """
    with open(output_path, 'w') as file:
        file.write(f"rows={rows}\n")
        file.write(f"cols={cols}\n")
        for result in results:
            file.write(f"({result[0]}, {result[1]}, {result[2]})\n")

if __name__ == "__main__":
    print("\n\033[1m\033[31m....................\033[32mWelcome To Sparix Matrix\033[31m...............\n")
    input_file_path = input("\033[1m\033[34mEnter the path of the first matrix file: ")
    print("\033[1mReading File Wait...\033[0m")
    matrix1 = process_input_file(input_file_path)
    print('\033[1m\033[33m\n\n#*-->' * 2, "\033[32mDone Reading file 1:",input_file_path, '\033[0m\n\n')
    second_file_path = input("\033[1m\033[34mEnter the path of the second matrix file: ")    
    if input_file_path == second_file_path:
       matrix2 = matrix1
    else:
       print("Reading File Wait...")
       matrix2 = process_input_file(second_file_path)
    print('\n\n#*-->' * 2, "\033[33mDone Reading file 2:",second_file_path, '\033[0m\n\n')
    output_file_path = input("\033[1m\033[34mEnter the Name for the output file: ")   
    print("*************************----Welcome To Our system:*********************************")
    print("Which operation would you like to perform on your matrix:\n")
    print("\033[1m\033[31ma. Multiply matrices")
    print("\033[1m\033[32mb. Subtract matrices")
    print("\033[1m\033[33mc. Add matrices\n")
    choice = input("\033[1m\033[30mEnter your choice: ")

    if choice == 'c':
       result = matrix1.add_matrices(matrix2)
       output_results(output_file_path, result.data, result.rows, result.cols)
       print("\033[1m\033[32mDone Saving Your Output Data..")
    elif choice == 'b':
       result = matrix1.subtract_matrices(matrix2)
       output_results(output_file_path, result.data, result.rows, result.cols)
       print("\033[1m\033[32mDone Saving Your Output Data..")
    elif choice == 'a':
       result = matrix1.multiply_matrices(matrix2)
       output_results(output_file_path, result.data, result.rows, result.cols)
       print("\033[1m\033[32mDone Saving Your Output Data..")
    else:
       print("Enter Valid choose.")