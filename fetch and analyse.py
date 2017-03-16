import pdb, urllib.request, sys, json, statistics, scipy, numpy, pprint
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np


fetch_url = "http://localhost/results/latest_n_for_device/1000/results"

def heatmap(results):

    a = np.array(results)

    plt.imshow(a, cmap='hot', interpolation='nearest')
    plt.ylabel('Row scan number')
    plt.xlabel('Pressure-pixel column')
    plt.title('Pressure pixel ADC readings over time')
    plt.rcParams['axes.facecolor']='white'
    plt.show()


def fetch_results(url):
    response = urllib.request.urlopen(url)
    injson = json.loads(response.read().decode('ascii'))

    resp_dict = {}

    for i in injson["responses"]:

        two_d = [x.split(" ") for x in i["raw_results"].split("\r\n")] #convert to 2d array 
        res = []
        for j in two_d:
            res.append([int(x) for x in j if x is not ''])

        entry = (i["id"], res)

        if i["tag"] in resp_dict.keys():
            resp_dict[i["tag"]].append(entry)
        else:
            resp_dict[i["tag"]] = [entry]
    return resp_dict
        
def sum_columns(result):
    col_width = len(result[0])
    sums = [0]*col_width
    for i in result:
        for j in range(0, col_width):
            if i[j] is not '': sums[j] += i[j]

    return sums

def find_max_column(result):
    return result.index(max(result))

def find_num_results(result):
    return len(result)

def get_column_from_result(result, col):
    result_length = find_num_results(result)
    transpose = []

    for i in range(0, result_length):
        transpose.append(result[i][col])

    return transpose

def average_column(result, col):
    result_length = find_num_results(result)
    transpose = get_column_from_result(result, col)

    return sum(transpose)/result_length


def all_results_ave_num_by_tag(results):

    num_results = {}
    for key in results.keys():
        lens = [len(x[1]) for x in results[key]] #count the length of each result set in the tag group
        num_results[key] = {"mean":   scipy.mean(lens),
                            "stddev": scipy.std(lens)}

    return num_results

def all_results_sum_cols_by_tag(data):
    results = {}


    for key in data.keys():
        pass


    return num_results

def all_results_max_col_stats_by_tag(data):
    results = {}

    for key in data.keys():
        max_val_col = []
        all_vals = []

        for result in data[key]:
            max_val_col.append(get_column_from_result(result[1], find_max_column(sum_columns(result[1]))))
            all_vals.append(result[1])

        #flatten arrays to 1d
        max_val_col = numpy.concatenate(max_val_col).ravel()
        all_vals = numpy.concatenate(all_vals).ravel()

        results[key] = {"max_col_mean": scipy.mean(max_val_col), "max_col_stdev": scipy.std(max_val_col), "max_col_n": max_val_col.size,
                        "all_val_mean": scipy.mean(all_vals), "all_val_stdev": scipy.std(all_vals), "all_val_n": all_vals.size}

    return results


def all_results_max_col_stats_by_tag_filter_res_len(data, minlen, maxlen):
    results = {}

    for key in data.keys():
        max_val_col = []
        all_vals = []

        for result in data[key]:
            if len(result[1]) > minlen and len(result[1]) < maxlen:
                max_val_col.append(get_column_from_result(result[1], find_max_column(sum_columns(result[1]))))
                all_vals.append(result[1])

        #flatten arrays to 1d
        max_val_col = numpy.concatenate(max_val_col).ravel()
        all_vals = numpy.concatenate(all_vals).ravel()

        results[key] = {"max_col_mean": scipy.mean(max_val_col), "max_col_stdev": scipy.std(max_val_col), "max_col_n": max_val_col.size,
                        "all_val_mean": scipy.mean(all_vals), "all_val_stdev": scipy.std(all_vals), "all_val_n": all_vals.size}

    return results

def test_result_vs_stats(result, stat_dict):
    mean = scipy.mean(result)
    stdev = scipy.std(result)
    n = len(result)

    result_stats = {}
    for key in stat_dict.keys():
        result_stats[key] = stats.ttest_ind_from_stats(mean, stdev, n,
                                                             stat_dict[key]["mean"],
                                                             stat_dict[key]["std"],
                                                             stat_dict[key]["n"])
    return result_stats

def pp(result):
    pprint.PrettyPrinter().pprint(result)

def build_prototype_results(result_dict):
    prototype_dict = {}
    for key in result_dict.keys():
        prototype = []
        for result in result_dict[key]:
            max_col = find_max_column(sum_columns(result[1]))
            col = get_column_from_result(result[1], max_col)

            for i in range(0,len(col)):
                if len(prototype) == i:
                    prototype.append([col[i]])
                else:
                    prototype[i].append(col[i])
        ave_prototype = [scipy.mean(x) for x in prototype]
        prototype_dict[key] = {"prototype": ave_prototype,
                               "mean": scipy.mean(ave_prototype),
                               "std": scipy.std(ave_prototype),
                               "n": len(ave_prototype)}
    return prototype_dict       


    

results = fetch_results(fetch_url)

#keys: 'w:611g, d:89mm, h:85mm, name:mason_jar', 
#      'w:473g, d:75mm, h:108mm, name:red_beans', 
#      'w:252g, d:84mm, h:93mm, name:marmite',
#      'w:284g, d:66mm, h:96mm, name:nut_jar'

key = 'w:473g, d:75mm, h:108mm, name:red_beans'
#key = 'w:284g, d:66mm, h:96mm, name:nut_jar'
#key = 'w:252g, d:84mm, h:93mm, name:marmite'
#key ='w:611g, d:89mm, h:85mm, name:mason_jar',

#uncomment for heatmap of all results in a key
test_result = results[key][9][1]
for i in results[key]:
    heatmap(i[1])

#sum_c = sum_columns(test_result)
#num_c = find_num_results(test_result)
#mc = find_max_column(sum_c)
#ave = average_column(test_result, mc)
anbt = all_results_ave_num_by_tag(results)
asbt = all_results_max_col_stats_by_tag(results)
#asbtwf = all_results_max_col_stats_by_tag_filter_res_len(results,5,15)

ptr = build_prototype_results(results)

test_stats = test_result_vs_stats(test_result, ptr)
print("Average number of crossings per result:")
pp(anbt)
print("\n\nSummary statistics for all results:")
pp(asbt)
print("\n\n 2-sample T-test results comparing a test result from red_beans against the corpus")
pp(test_stats)

