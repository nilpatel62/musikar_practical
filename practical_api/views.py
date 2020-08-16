from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
import pandas as pd

class ConvertCsvFiles(APIView):
    def post(self, request):
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
                sum_of_numeric_coulmn = df1.sum(axis = 0, skipna = True, numeric_only=True) # count or get the sum of all numeric column
                print("sum of numeric coulmn", sum_of_numeric_coulmn)
                median_of_numeric_coulmn = df1.median(axis = 0, skipna = True, numeric_only=True) # count or get the median of all numeric column
                print("median of numeric coulmn", median_of_numeric_coulmn)
                mean_of_numeric_coulmn = df1.mean(axis = 0, skipna = True, numeric_only=True) # count or get the mean of all numeric column
                print("mean of numeric coulmn", mean_of_numeric_coulmn)
                mode_of_numeric_coulmn = df1.mean(axis = 0, skipna = True, numeric_only=True) # count or get the mode of all numeric column
                print("mode of numeric coulmn", mode_of_numeric_coulmn)
        return HttpResponse("Hello")