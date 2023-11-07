import numpy as np


# initializing random number generator
# https://numpy.org/doc/stable/reference/random/generator.html
rng = np.random.default_rng()


def generating_random_shape_for_2d_array():
    # generating random ints to use as rows and columns
    rows = rng.integers(low=3, high=11, dtype=np.int8)
    columns = rng.integers(low=7, high=16, dtype=np.int8)
    return rows, columns


def filling_2d_array_by_random_ints(rows, columns):
    # generating 2d array of ints with size of rows and columns
    result = rng.integers(low=-100, high=100, size=(rows, columns), dtype=np.int16)
    return result


def generating_random_2d_array_of_ints():
    rows, columns = generating_random_shape_for_2d_array()
    return filling_2d_array_by_random_ints(rows, columns)


def calculating_b_from_a(a):
    # the calculation function was agreed in the email
    return a * 2 + 5


# making calculating_a_from_b function vectorized
# https://numpy.org/doc/stable/reference/generated/numpy.vectorize.html
v_calculating_b_from_a = np.vectorize(calculating_b_from_a)


def creating_column_b_from_column_a(column_a):
    # creating column B from the values of column A by vectrorized function
    column_b = v_calculating_b_from_a(column_a)
    return column_b


def creating_cumulative_sum_column(column_a):
    # creating column with cumulative sum of values from column A
    # https://numpy.org/doc/stable/reference/generated/numpy.cumsum.html
    column_cum_sum = np.cumsum(column_a)
    return column_cum_sum


def adding_special_columns(arr):
    # making slice to get the last column of 2d array
    last_column = arr[:, -1]

    column_b = creating_column_b_from_column_a(last_column)
    column_cum_sum = creating_cumulative_sum_column(column_b)

    # making temporary 2d array of special columns
    temp = np.vstack([column_b, column_cum_sum])

    # concatenating original 2d array and temporary 2d array of special columns
    # https://numpy.org/doc/stable/reference/generated/numpy.concatenate.html
    # temp.T transposes temporary 2d array before concatenation
    # https://numpy.org/doc/stable/reference/generated/numpy.ndarray.T.html
    result = np.concatenate((arr, temp.T), axis=1)
    return result


def generating_random_data():
    # generating 2d array of random size and random ints and special columns
    return adding_special_columns(generating_random_2d_array_of_ints())


def resizing_2d_array_randomly(arr):
    rows, columns = generating_random_shape_for_2d_array()

    # 2 last columns are special. So we need to get quantity of columns in the original 2d array
    original_arr_columns = arr.shape[1] - 2

    # getting the original 2d array without 2 last special columns
    original_arr = arr[:, : original_arr_columns]

    # numpy.ndarray.resize works on single-segment arrays only
    # but after slicing we get non-contiguous array, so we have to make it contiguous
    # https://numpy.org/doc/stable/reference/generated/numpy.ascontiguousarray.html
    original_arr = np.ascontiguousarray(original_arr)

    # changing shape and size of array in-place
    # https://numpy.org/doc/stable/reference/generated/numpy.ndarray.resize.html
    original_arr.resize((rows, columns), refcheck=False)

    # calculating and concatenating back 2 special columns
    return adding_special_columns(original_arr)


def refilling_2d_array_randomly(arr):
    rows, columns = arr.shape

    # 2 last columns are special. So we need to subtract them from columns before refilling
    temp = filling_2d_array_by_random_ints(rows, columns - 2)

    # calculating and concatenating back 2 special columns
    return adding_special_columns(temp)
