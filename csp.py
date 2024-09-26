from typing import Any
from queue import Queue


class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
    ):
        """Constructs a CSP instance with the given variables, domains and edges.
        
        Parameters
        ----------
        variables : list[str]
            The variables for the CSP
        domains : dict[str, set]
            The domains of the variables
        edges : list[tuple[str, str]]
            Pairs of variables that must not be assigned the same value
        """
        self.variables = variables
        self.domains = domains
        self.edges = edges
        # Binary constraints as a dictionary mapping variable pairs to a set of value pairs.
        #
        # To check if variable1=value1, variable2=value2 is in violation of a binary constraint:
        # if (
        #     (variable1, variable2) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable1, variable2)]
        # ) or (
        #     (variable2, variable1) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable2, variable1)]
        # ):
        #     Violates a binary constraint
        self.binary_constraints: dict[tuple[str, str], set] = {}
        for variable1, variable2 in edges:
            self.binary_constraints[(variable1, variable2)] = set()
            for value1 in self.domains[variable1]:
                for value2 in self.domains[variable2]:
                    if value1 != value2:
                        self.binary_constraints[(variable1, variable2)].add((value1, value2))
                        self.binary_constraints[(variable1, variable2)].add((value2, value1))

    def ac_3(self) -> bool:
        """Performs AC-3 on the CSP.
        Meant to be run prior to calling backtracking_search() to reduce the search for some problems.
    
        Returns
        -------
        bool
            False if a domain becomes empty, otherwise True
        """
    
        queue = []
        for variable in self.variables:
            for edge in self.edges:
                queue.append((variable, edge))

        while len(queue)>0:
            Xi, Xj = queue.pop(0)
            if Revise(self, Xi, Xj):
                for Xk in Xi.edges:
                    if Xk != Xj:
                        queue.append((Xk, Xi))
        return True
    
def Revise(self, Xi, Xj):
    revised = False
    print("Xi:_ " , Xi)
    print("Xj: ", Xj)
    for x in self.domains:
        print("X = ", x)
        for value in x:
            print("Value :" , value)
            if not isConstraint(self, x, value, self.domains):
                Xi.domain.remove(x)
                revised=True
    return revised


    def backtracking_search(self) -> None | dict[str, Any]:
        """Performs backtracking search on the CSP.
        
        Returns
        -------
        None | dict[str, Any]
            A solution if any exists, otherwise None
        """
        def backtrack(assignment: dict[str, Any]):
            if(len(assignment) == len(self.variables)):
                return assignment
            # YOUR CODE HERE (and remove the assertion below)
            
            var = selectUnassignedVariable(self, assignment)
            #print("Select unassigned variable = " , var)
    
            valueList = orderDomainValues(self, var, assignment)
            for value in valueList:
                #print("Value før constraint ", value)
                if not isConstraint(self, var, value, assignment):
                   #print("Legg til verdi i assignemnt")
                    assignment[var] = value
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                    
                    assignment.pop(var)
            return None
            #assert False, "Not implemented"
            #print("Returnerer assignment", assignment)
        return backtrack({})

def selectUnassignedVariable(self, assignment):
    for var in self.variables:
        if var not in assignment:
            return var
        
def isConstraint(self, var, value, assignment):
    for var2, value2 in assignment.items():
        #print("!!!!!!!!!!!")
        #print(var2, "______", value2)

        if (
            (var, var2) in self.binary_constraints and
            (value, value2) not in self.binary_constraints[(var, var2)]
        ) or (
            (var2, var) in self.binary_constraints and
            (value, value2) not in self.binary_constraints[(var2, var)]
        ):
            return True
    return False  
        
def orderDomainValues(self, var, assignment):
    lists = []
    for value in self.domains[var]:
        lists.append(value)
    return lists


def alldiff(variables: list[str]) -> list[tuple[str, str]]:
    """Returns a list of edges interconnecting all of the input variables
    
    Parameters
    ----------
    variables : list[str]
        The variables that all must be different

    Returns
    -------
    list[tuple[str, str]]
        List of edges in the form (a, b)
    """
    return [(variables[i], variables[j]) for i in range(len(variables) - 1) for j in range(i + 1, len(variables))]
