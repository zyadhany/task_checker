#include "stdio.h"

void sort(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (arr[i] > arr[j]) {
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
    }
}

int main() {
    int n;
    scanf("%i", &n);

    int arr[10];

    for (int i = 0; i < n; i++) {
        scanf("%i", &arr[i]);
    }
    sort(arr, n);

    for (int i = 0; i < n; i++) {
        printf("%i ", arr[i]);
    }
    printf("\n");
    return 0;
}
