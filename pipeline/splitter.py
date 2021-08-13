from collections import OrderedDict
import time
import datetime


class Expression(object):

    def __init__(self, filter):

        self.filter = filter
        self.operators_dict = {"and": "and", "or": "or", "eq": "==",   # we can save it in config and get this info from config
                               "gt": ">", "ge": ">=", "lt": "<",
                               "le": "<=", "between": "between",
                               "is_null": "is_null", "not": "not",
                               "in": "in"}
        self.multiple_condition_operators = ["and", "or", "not"]
        self.negative_operator = []
        self._count = 0

    def FILTER(self, new_filter=None):

        if new_filter:
            self.filter = new_filter

        return self.filter

    def resolve(self, filter: str = None):

        if filter:
            self.filter = self.FILTER(new_filter=filter)

        result = self.check_operator(filter=self.FILTER(), work_dir=None)

        if isinstance(result, dict):
            result = [result]

        return result

    def check_operator(self, filter, work_dir):

        if len(filter.split("(")) == 1:

            return "Bad filter"

        operator = filter.split("(")[0]

        if operator in self.multiple_condition_operators:

            filter = filter[len(operator) + 1:-1]

            operator = self.operators_dict.get(operator)

            if self._count == 0:

                work_instance = [{operator: []}]
                # print(work_instance)
                work_dir = work_instance[0][operator]
                self._count += 1

            else:

                work_instance = {operator: []}
                # print(work_instance)
                work_dir = work_instance[operator]

            sub_filter = self.check_operator(filter=filter, work_dir=None)

            if isinstance(sub_filter, list):
                for item in sub_filter:
                    work_dir.append(item)

            else:
                work_dir.append(sub_filter)

            return work_instance

        else:

            list_of_filters = self.parse_one_two_expr(filter=filter)

            return list_of_filters

    def create_dict(self, filter: str):

        operator = filter.split("(")[0]
        # print(f">>>Filter: {filter}")
        split_filter = filter[len(operator) + 1:-1].split(",")
        # print(f"SPLIT FILTER IN CREATE_DICT: {split_filter}")
        operator = self.operators_dict.get(operator)

        if operator == "between":

            filter = {"field": split_filter[0].strip(), "op": operator,
                      'values': [self.check_value_type(value=split_filter[1].strip()),
                                 self.check_value_type(value=split_filter[2].strip())]}

        elif operator == "in":

            value_list = []
            for value in split_filter[1:]:
                value_list.append(self.check_value_type(value=value.strip()))

            filter = {"field": split_filter[0].strip(), "op": operator,
                      'values': value_list}

        elif operator in ["is_null"]:

            filter = {"field": split_filter[0].strip(), "op": operator}

        else:

            filter = {"field": split_filter[0].strip(), "op": operator,
                      'value': self.check_value_type(value=split_filter[1].strip())}
            print(filter.get("value"))
            print(type(self.check_value_type(value=split_filter[1].strip())))
        return filter

    def parse_one_two_expr(self, filter: str):

        list_of_filters = []

        filters = filter.split("),")
        # print(f"filters list: {filters}")

        if len(filters) == 1:

            filter_dict = self.create_dict(filter=filters[0])
            return filter_dict

        list_number = 1

        for filter_str in filters:

            if filters[-1] != filter_str:
                # filter_str = filter_str+" "
                filter_str = filter_str + (" " * list_number)

            list_of_filters.append(self.check_operator(work_dir=dict(), filter=filter_str))
            list_number +=1
        return list_of_filters

    def and_or(self, work_dir, pointer, filter, operator):

        work_dir.append(dict())
        work_dir[pointer][self.operators_dict.get(operator)] = list()
        self.FILTER(new_filter=filter[len(operator) + 1:-1])

        return work_dir

    @staticmethod
    def check_value_type(value):

        try:
            return int(value)

        except ValueError:
            pass

        try:
            return float(value)

        except ValueError:
            pass

        try:

            return datetime.datetime.strptime(value[1:-1], '%Y-%m-%d').date()

        except ValueError:
            pass

        try:

            return datetime.datetime.strptime(value[1:-1], '%Y-%m-%dT%H:%M:%S')

        except ValueError:
            pass

        try:
            return bool(value)

        except ValueError:
            pass

        return value


print("test_0")
test_0 = Expression(filter="124").resolve()
print(test_0)

print("test_1")
test_1 = Expression(filter="eq(startDate,'2021-01-03')").resolve()
print(test_1)

print("test_2")
test_2 = Expression(filter="between(startDate,'2021-01-03','2021-04-20')").resolve()
print(test_2)

print("test_3")
test_3 = Expression(filter="not(eq(startDate,'2021-01-03'))").resolve()
print(test_3)

print("test_4")
test_4 = Expression(filter="not(between(startDate,'2021-01-03','2021-04-20'))").resolve()
print(test_4)

print("test_5")
test_5 = Expression(filter="and(gt(ownerName,Mike(Senczyk)),between(startDate,'2021-01-03','2021-04-20'))").resolve()
print(test_5)

print("test_6")
test_6 = Expression(filter="and(gt(ownerName,Mike(Senczyk)),or(between(startDate,'2021-01-03','2021-04-20'),not(gt(ownerName,Mike(Senczyk)))))").resolve()
print(test_6)

print("test7")
test_7 = Expression(filter="and(eq(startDate,'2021-05-23T11:23:23'),gt(ownerName,55),not(between(startDate,'2021-01-03','2021-04-20')))").resolve()
print(test_7)

print("test_8")
test_8 = Expression(filter="and(eq(startDate,'2021-05-23T11:23:23'),gt(ownerName,55),not(in(startDate,'2021-01-03','2021-04-20','2021-04-22')))").resolve()
print(test_8)
