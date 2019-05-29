class PerformanceData:

    def __init__(self, table=None):
        if table is None:
            table = []
        self.table = table
        self.means = []
        self.name = ""
        self.folds = 0
        self.runs = 0
        pass

    # Load data from Weka experimenter csv output and store percentage of hits of each fold per each run.
    def load_data_from_weka_results(self, name, folds, runs):
        self.name = name
        file = open(self.name, "r")
        lines = file.readlines()
        accuracies = []
        self.folds = folds
        self.runs = runs
        # Read accuracies from file.
        for i in range(1, len(lines)):
            accuracy = float(lines[i].split(";")[12])
            accuracies.append(accuracy)
        file.close()

        bunch = []
        # Insert each bunch of folds accuracies in runs
        for i in range(0, self.runs*self.folds):
            if i != 0 and i % self.folds == 0:
                self.table.append(bunch.copy())
                bunch.clear()
            bunch.append(accuracies[i])
        self.table.append(bunch.copy())
        bunch.clear()

    # Print all runs.
    def print_runs(self):
        for run in self.table:
            print(run)

    # Order runs per fold value. (Low to High).
    def order_folds_in_runs(self):
        for run in self.table:
            run.sort()

    # Write csv file with stored runs.
    def write_csv(self):
        if self.name == "":
            self.name = "subtracted"
        file = open(self.name + "-ordered.csv", "w+")
        line = ""
        for run in self.table:
            for val in run:
                line = line + str(val) + ";"
            line = line[:-1]
            file.write(line+"\n")
            line = ""
        pass

    # Calculate mean per each fold.
    def calculate_means_per_fold_ordered(self):
        means = [0] * len(self.table)
        for run in self.table:
            i = 0
            for val in run:
                means[i] += val
                i += 1
        for i in range(0, len(means)):
            means[i] /= len(self.table)
        self.table.append(means)

        self.means = means

        print(means)

    # Subtract another
    def subtract(self, data):
        res = []
        for i in range(0, len(self.table)):
            bunch10 = []
            for j in range(0, len(self.table[i])):
                bunch10.append(self.table[i][j] - data.get_table()[i][j])
            res.append(bunch10)
        return res

    # Get generated table
    def get_table(self):
        return self.table

    # Set a table.
    def set_table(self, table):
        self.table = table

    def get_means(self):
        return self.means
