
import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
from scipy import stats

from PerformanceData import PerformanceData


def main():
    print("Load BayesNet data:")
    data1 = PerformanceData()
    data1.load_data_from_weka_results("BayesNet.csv", 10, 10)
    data1.print_runs()
    print("")
    print("Load J48 data:")
    data2 = PerformanceData()
    data2.load_data_from_weka_results("J48.csv", 10, 10)
    data2.print_runs()
    print("")

    print("Calculate subtraction:")
    data3 = PerformanceData(data1.subtract(data2))
    data3.print_runs()
    data3.order_folds_in_runs()
    print("")
    print("Calculate means:")
    data3.calculate_means_per_fold_ordered()
    data3.write_csv()
    print("")

    true_mu = 0  # Null hypothesis.

    print("Shapiro-Wilk test results:")
    print(stats.shapiro(data3.get_means()))
    print("")

    print("t-test results:")
    print(scipy.stats.ttest_1samp(data3.get_means(), true_mu))
    print("")

    generate_histogram(data3.get_means())


def generate_histogram(data):
    # example data
    mu = np.mean(data)  # mean of distribution
    sigma = np.std(data)  # standard deviation of distribution

    num_bins = 20

    fig, ax = plt.subplots()

    # the histogram of the data
    n, bins, patches = ax.hist(data, num_bins, density=1)

    # add a 'best fit' line
    y = stats.norm.pdf(bins, mu, sigma)
    ax.plot(bins, y, '--', color="red")
    ax.set_xlabel('Subtraction Value')
    ax.set_ylabel('Frequency')
    ax.set_title(r'Histogram of Subtraction Values: μ=' + '{:.2f}'.format(mu) + ', σ=' + '{:.2f}'.format(sigma))
    ax.axvline(x=mu, color="red")
    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.show()

main()