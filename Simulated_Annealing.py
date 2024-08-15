import random
import math

SPACER = '--------------------------------------------------------------------'



class SimulatedAnnealing(object):

    def __init__(self, start_temperature, stop_temperature, alpha, iterations_number, temperature_method='geometric', print_xn=True, print_probabilities=True):
        self.start_temperature = start_temperature
        self.stop_temperature = stop_temperature
        self.alpha = alpha
        self.iteration_number = iterations_number
        self.temperature_method = temperature_method
        self.print_xn = print_xn
        self.print_probabilities = print_probabilities
    def probability_function(self, delta, t_new):
        p = math.exp((delta / t_new) * (-1))
        if self.print_probabilities:
            print(f'Probability of Acceptance: {p}%')
        r = random.random()
        decision = p - r
        if decision >= 0:
            return True
        else:
            return False

    def constant_reduce_temp(self, k):
        return self.start_temperature - 1.5 * k

    def logarithmic_temp(self, k):
        return (self.alpha * self.start_temperature) / (1 + math.log(k))

    def geometric_temp(self, k):
        return self.alpha ** k * self.start_temperature

    def exponential_temp(self, k, n):
        return self.start_temperature * math.e ** (self.alpha * (-1) * k ** (1 / n))
    def multiple_annealing(self,number:int,dimension, function, finding_neighbor_func, initial_random_func, initial_point=None, minimum=None, print_iterations=True):
        if number<1:
            return None, None
        if print_iterations:
            print(f"iteration 1")
        best_result,best_point = self.start_annealing(dimension,function,finding_neighbor_func,initial_random_func,initial_point=initial_point,minimum=minimum)
        for i in range(number):
            if print_iterations:
                print(f"iteration {i}")
            cost, point = self.start_annealing(dimension,function,finding_neighbor_func,initial_random_func,initial_point=initial_point,minimum=minimum)
            if cost<best_result:
                best_result = cost
                best_point = point
        return best_result, best_point
    def start_annealing(self, dimension, function, finding_neighbor_func, initial_random_func, initial_point=None, minimum=None):
        if initial_point is None:
            point = initial_random_func()
        else:
            point = initial_point

        c_old = function(point)
        t_new = self.start_temperature
        counter = 0

        print(f'Starting algorithm with {self.iteration_number} iterations and {t_new} temperature')
        print("Initial Cost: " + str(c_old))
        print(SPACER)

        while t_new > self.stop_temperature and counter <= self.iteration_number:
            if self.print_probabilities:
                print(f'Iteration number: {counter}')
            new_point = finding_neighbor_func(point.copy())
            c_new = function(new_point)

            if minimum is not None:
                if c_new == minimum:
                    c_old = c_new
                    point = new_point
                    break

            delta = c_new - c_old
            if self.print_probabilities:
                print(f'delta: {delta} ')
                print(f'Old Cost: {c_old}')

            if delta <= 0:
                if self.print_probabilities:
                    print('The new solution is better')
                point = new_point
                c_old = c_new

            else:
                if self.print_probabilities:
                    print('The new solution is worse')
                decision = self.probability_function(delta=delta, t_new=t_new)

                if decision == True:
                    if self.print_probabilities:
                        print('But the probability function accept it!')
                    point = new_point
                    c_old = c_new

                else:
                    if self.print_probabilities:
                        print('Neighbor is rejected by the probability function')

            if self.print_xn == True:
                for i in range(dimension):
                    if self.print_probabilities:
                        print(f'x{i}_old = ' + str(point[i]))
            if self.print_probabilities:
                print("New Cost = " + str(c_new))
            if self.temperature_method.lower().strip() == 'logarithmic':
                t_new = self.logarithmic_temp(counter+1)

            elif self.temperature_method.lower().strip() == 'geometric':
                t_new = self.geometric_temp(counter)

            elif self.temperature_method.lower().strip() == 'exponential':
                t_new = self.exponential_temp(counter, dimension)

            elif self.temperature_method.lower().strip() == 'constant':
                t_new = self.constant_reduce_temp(counter)

            # you can implant new methods to calculate temperature here
            if self.print_probabilities:
                print(SPACER)
                print('New Temperature = ' + str(t_new))
                print(SPACER)
            counter += 1

        print(f"The answer after {counter} iterations is {c_old}")
        print(SPACER)
        return c_old, point