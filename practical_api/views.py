from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
import pandas as pd
from csv import reader, writer
import os
import locale
from collections import defaultdict
import math


class ConvertCsvFiles(APIView):
    def post(self, request):
        try:
            data = request.data
            file_url = data['fileUrl']
            flag = data['flag'] if "flag" in data else 1
            if file_url == "":
                response = {
                    "message": "file url is empty"
                }
                return JsonResponse(response, safe=False, status=422)
            else:
                if int(flag) == 1:
                    dataframe = pd.read_csv(file_url, sep=',')
                    dataframe.columns = dataframe.iloc[0] # get the headers as a 1st column no need to change that
                    dataframe = dataframe.reindex(dataframe.index.drop(0)).reset_index(drop=True) # change the or swap the column to row and row to column
                    dataframe.columns.name = None # change column name to none
                    df1 = dataframe.dropna(axis=1) # remove all null or None value from the dataframe

                    # code for the 1st operation for the task
                    sum_of_numeric_coulmn = df1.sum(axis = 0, skipna = True, numeric_only=True) # count or get the sum of all numeric column
                    print("sum of numeric coulmn", sum_of_numeric_coulmn)

                    # code for the 2nd operation for the task
                    median_of_numeric_coulmn = df1.median(axis = 0, skipna = True, numeric_only=True) # count or get the median of all numeric column
                    print("median of numeric coulmn", median_of_numeric_coulmn)
                    mean_of_numeric_coulmn = df1.mean(axis = 0, skipna = True, numeric_only=True) # count or get the mean of all numeric column
                    print("mean of numeric coulmn", mean_of_numeric_coulmn)
                    mode_of_numeric_coulmn = df1.mean(axis = 0, skipna = True, numeric_only=True) # count or get the mode of all numeric column
                    print("mode of numeric coulmn", mode_of_numeric_coulmn)

                    # code for the 3rd operation for the task
                    deviation_of_numeric_coulmn = df1.std(ddof=0, axis = 0, skipna = True, numeric_only=True) # count or get the Deviation of all numeric column
                    print("Deviation of numeric coulmn", deviation_of_numeric_coulmn)
                    variance_of_numeric_coulmn = df1.var(ddof=0, axis = 0, skipna = True, numeric_only=True) # count or get the Variance of all numeric column
                    print("Variance of numeric coulmn", variance_of_numeric_coulmn)

                    # code for the 4th operation for the task
                    quantile_of_10_numeric_coulmn = df1.quantile(0.1, axis = 0, numeric_only=True) # count or get the quantile of all numeric column for 10th Percentile
                    print("quantile of 10 numeric coulmn", quantile_of_10_numeric_coulmn)
                    quantile_of_90_numeric_coulmn = df1.quantile(0.9, axis = 0, numeric_only=True) # count or get the quantile of all numeric column for 90th Percentile
                    print("quantile of 90 numeric coulmn", quantile_of_90_numeric_coulmn)
                else:
                    d = defaultdict(list)
                    with open(file_url) as f, open('destination.csv', 'w') as fw:
                        writer(fw, delimiter=',').writerows(zip(*reader(f, delimiter=',')))
                    with open("destination.csv") as fin:
                        # calculate the total sum of the numeric value
                        total = 0
                        average = 0
                        Sum = 0
                        for row in reader(fin):
                            try:
                                d[row[1]].append(float(row[2]))
                            except:
                                pass
                            try:
                                for col in row[1]:
                                    total += int(col)
                            except:
                                pass
                        # ======================end for sum the data=====================================

                    # ===================for the second step=============================================
                    mediun_data = 0
                    mean_data = 0
                    mode_data = 0
                    percentile_10_th = 0
                    percentile_90_th = 0
                    for k,v in d.items():
                        try:
                            mediun_data = sorted(v)[len(v) // 2] + mediun_data
                            mean_data = sum(v)/len(v) + mean_data
                            mode_data = list(set(v))[0] + mode_data
                            size = len(v)
                            percentile_10_th = sorted(v)[int(math.ceil((size * 10) / 100)) - 1] + percentile_10_th
                            percentile_90_th = sorted(v)[int(math.ceil((size * 90) / 100)) - 1] + percentile_90_th
                        except:
                            pass
                    print("Median is", mediun_data)
                    print("Mean is", mean_data)
                    print("mode value", mode_data)
                    print("10th percentile", percentile_10_th)
                    print("90th percentile", percentile_90_th)
                    os.remove("destination.csv")

                response = {
                    "message": "data processing done"
                }
                return JsonResponse(response, safe=False, status=200)
        except:
            response = {
                "message": "Internal Server Error"
            }
            return JsonResponse(response, safe=False, status=500)