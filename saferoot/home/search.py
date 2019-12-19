def binarySearch(arr, l, r, x):
    # Check base case
    if r >= l:

        mid = l + (r - l) / 2
        mid = int(mid)

        # If element is present at the middle itself
        if compare(arr, mid, x):
            return mid

            # If element is smaller than mid, then it
        # can only be present in left subarray
        elif arr[mid] > x:
            return binarySearch(arr, l, mid - 1, x)

            # Else the element can only be present
        # in right subarray
        else:
            return binarySearch(arr, mid + 1, r, x)

    else:
        # Element is not present in the array
        return -1


def compare(arr, current_index, x):
    if len(arr) == current_index+1:
        return True
    return arr[current_index] <= x <= arr[current_index+1]
