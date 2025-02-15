'''pca_cov.py
Performs principal component analysis using the covariance matrix of the dataset
Maya Purohit
CS 251: Data Analysis and Visualization
Fall 2023
'''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from data_transformations import normalize, center


class PCA:
    '''Perform and store principal component analysis results

    NOTE: In your implementations, only the following "high level" `scipy`/`numpy` functions can be used:
    - `np.linalg.eig`
    The numpy functions that you have been using so far are fine to use.
    '''

    def __init__(self, data):
        '''

        Parameters:
        -----------
        data: pandas DataFrame. shape=(num_samps, num_vars)
            Contains all the data samples and variables in a dataset. Should be set as an instance variable.
        '''
        self.data = data

        # vars: Python list. len(vars) = num_selected_vars
        #   String variable names selected from the DataFrame to run PCA on.
        #   num_selected_vars <= num_vars
        self.vars = None

        # A: ndarray. shape=(num_samps, num_selected_vars)
        #   Matrix of data selected for PCA
        self.A = None

        # normalized: boolean.
        #   Whether data matrix (A) is normalized by self.pca
        self.normalized = None

        # A_proj: ndarray. shape=(num_samps, num_pcs_to_keep)
        #   Matrix of PCA projected datacenter
        self.A_proj = None

        # e_vals: ndarray. shape=(num_pcs,)
        #   Full set of eigenvalues (ordered large-to-small)
        self.e_vals = None
        # e_vecs: ndarray. shape=(num_selected_vars, num_pcs)
        #   Full set of eigenvectors, corresponding to eigenvalues ordered large-to-small
        self.e_vecs = None

        # prop_var: Python list. len(prop_var) = num_pcs
        #   Proportion variance accounted for by the PCs (ordered large-to-small)
        self.prop_var = None

        # cum_var: Python list. len(cum_var) = num_pcs
        #   Cumulative proportion variance accounted for by the PCs (ordered large-to-small)
        self.cum_var = None

        # orig_means: ndarray. shape=(num_selected_vars,)
        #   Means of each orignal data variable
        self.orig_means = None

        # orig_mins: ndarray. shape=(num_selected_vars,)
        #   Mins of each orignal data variable
        self.orig_mins = None

        # orig_maxs: ndarray. shape=(num_selected_vars,)
        #   Maxs of each orignal data variable
        self.orig_maxs = None

        # self.pMat: ndarray. shape=(num_selected_vars, num_pcs_kept)
        #   rotation matrix into the PC space
        self.pMat = None
        


    def get_prop_var(self):
        '''(No changes should be needed)'''
        return self.prop_var

    def get_cum_var(self):
        '''(No changes should be needed)'''
        return self.cum_var

    def get_eigenvalues(self):
        '''(No changes should be needed)'''
        return self.e_vals

    def get_eigenvectors(self):
        '''(No changes should be needed)'''
        return self.e_vecs

    def covariance_matrix(self, data):
        '''Computes the covariance matrix of `data`

        Parameters:
        -----------
        data: ndarray. shape=(num_samps, num_vars)
            `data` is NOT centered coming in, you should do that here.

        Returns:
        -----------
        ndarray. shape=(num_vars, num_vars)
            The covariance matrix of centered `data`

        NOTE: You should do this wihout any loops
        NOTE: np.cov is off-limits here — compute it from "scratch"!
        '''


        centerData = center(data) #centers the data 
        covarianceMat = (centerData.T @ centerData) / (len(centerData) -1) #calculates the covariance matrix 

        return covarianceMat

    def compute_prop_var(self, e_vals):
        '''Computes the proportion variance accounted for by the principal components (PCs).

        Parameters:
        -----------
        e_vals: ndarray. shape=(num_pcs,)

        Returns:
        -----------
        Python list. len = num_pcs
            Proportion variance accounted for by the PCs
        '''

        prop_var = e_vals / e_vals.sum() #takes each of the eigenvalues and divides it by the sum of the eigenvalues 

        prop_var = prop_var.tolist() #convert it to a list 

        return prop_var


        

    def compute_cum_var(self, prop_var):
        '''Computes the cumulative variance accounted for by the principal components (PCs).

        Parameters:
        -----------
        prop_var: Python list. len(prop_var) = num_pcs
            Proportion variance accounted for by the PCs, ordered largest-to-smallest
            [Output of self.compute_prop_var()]

        Returns:
        -----------
        Python list. len = num_pcs
            Cumulative variance accounted for by the PCs
        '''

        cumVar = []

        for i in range(len(prop_var)):
            cumVar.append(sum(prop_var[0:i+1])) #adds each of the proportions that came before the proportion at the ith position to the proportion ith position
            

        return cumVar

        

    def pca(self, vars, normalize_dataset=False):
        '''Performs PCA on the data variables `vars`

        Parameters:
        -----------
        vars: Python list of strings. len(vars) = num_selected_vars
            1+ variable names selected to perform PCA on.
            Variable names must match those used in the `self.data` DataFrame.
        normalize_dataset: boolean.
            If True, min-max normalize each data variable it ranges from 0 to 1.

        NOTE: Leverage other methods in this class as much as possible to do computations.

        TODO:
        - Select the relevant data (corresponding to `vars`) from the data pandas DataFrame
        then convert to numpy ndarray for forthcoming calculations.
        - If `normalize` is True, normalize the selected data so that each variable (column)
        ranges from 0 to 1 (i.e. normalize based on the dynamic range of each variable).
            - Before normalizing, create instance variables containing information that would be
            needed to "undo" or reverse the normalization on the selected data.
        - Make sure to compute everything needed to set all instance variables defined in constructor,
        except for self.A_proj (this will happen later).

        '''

        self.A = self.data[vars].to_numpy()#converts the relevant data to a numpy array 
        self.vars = vars #holds the vars that we are analyzing
        self.normalized = normalize_dataset #is the data normalized in PCA?
        self.orig_maxs = self.A.max(axis = 0) #holds the original maxs, mins and means 
        self.orig_mins = self.A.min(axis = 0)
        self.orig_means = self.A.mean(axis = 0)
        

        if(normalize_dataset == True):
            self.A = (self.A - self.A.min(axis = 0)) / (self.A.max(axis = 0) - self.A.min(axis = 0)) #if normalize is true, perform min max normalization at data
            self.orig_means = self.A.mean(axis = 0)

        covMat = self.covariance_matrix(self.A) # makes the covariance matrix 
        eig_vals, eig_vecs = np.linalg.eig(covMat) #finds the eigenvectors 
        indexes = np.argsort(eig_vals)[::-1] #sort the eigenvalues from highest to lowest 
        self.e_vals = eig_vals[indexes] #sorts based on the indexes 
    
        self.e_vecs = eig_vecs[:,indexes] #sorts the columns based on the eigenvalues 
        self.prop_var = self.compute_prop_var(self.e_vals) #sets the prop var
        self.cum_var = self.compute_cum_var(self.prop_var) #sets the cumulative var 


    def elbow_plot(self, num_pcs_to_keep=None):
        '''Plots a curve of the cumulative variance accounted for by the top `num_pcs_to_keep` PCs.
        x axis corresponds to top PCs included (large-to-small order)
        y axis corresponds to proportion variance accounted for

        Parameters:
        -----------
        num_pcs_to_keep: int. Show the variance accounted for by this many top PCs.
            If num_pcs_to_keep is None, show variance accounted for by ALL the PCs (the default).

        NOTE: Make plot markers at each point. Enlarge them so that they look obvious.
        NOTE: Reminder to create useful x and y axis labels.
        NOTE: Don't write plt.show() in this method
        '''


        if self.cum_var is None:
            raise ValueError('Cant plot cumulative variance. Compute the PCA first.')
        
        else:
            if(num_pcs_to_keep == None):
                num = len(self.e_vecs)
                x = list(range(1,len(self.e_vecs)+1)) #chooses all of the pcs
                y = self.cum_var #chooses all of the cum var

            else:
                num = num_pcs_to_keep
                x = list(range(1, num_pcs_to_keep + 1)) #range until the number of pcs we want to keep 
                y = self.cum_var[:num_pcs_to_keep] #only chooses until the index of the number we want to keep 
            
            plt.plot(x, y) #plots the x and y that were chosen with axis titles 
            plt.scatter(x,y, color = "k", s= 40)
            plt.xlabel("PC Number")
            plt.ylabel("Cumulative Variance")
            plt.title("Cumulative Variance for PC's (" + str(num)+ ")")
            for i in range(len(x)): #add a label to each point stating its values 
                plt.annotate("(" + str(round(x[i],4)) + ", " + str(round(y[i], 4))+ ")",(x[i], y[i]), fontsize = 12)

    def pca_project(self, pcs_to_keep):
        '''Project the data onto `pcs_to_keep` PCs (not necessarily contiguous)

        Parameters:
        -----------
        pcs_to_keep: Python list of ints. len(pcs_to_keep) = num_pcs_to_keep
            Project the data onto these PCs.
            NOTE: This LIST contains indices of PCs to project the data onto, they are NOT necessarily
            contiguous.
            Example 1: [0, 2] would mean project on the 1st and 3rd largest PCs.
            Example 2: [0, 1] would mean project on the two largest PCs.

        Returns
        -----------
        pca_proj: ndarray. shape=(num_samps, num_pcs_to_keep).
            e.g. if pcs_to_keep = [0, 1],
            then pca_proj[:, 0] are x values, pca_proj[:, 1] are y values.

        NOTE: This method should set the variable `self.A_proj`

        '''

        p = self.e_vecs[np.ix_(np.arange(self.e_vecs.shape[0]), pcs_to_keep)] #makes the roation matrix with the pcs we want to keep
        self.pMat = p

        pca_proj = center(self.A) @ p #calculate the projection matrix by multiplying the centered A by the rotation matrix
        self.A_proj = pca_proj

        return self.A_proj



    def pca_then_project_back(self, top_k):
        '''Project the data into PCA space (on `top_k` PCs) then project it back to the data space

        (Week 2)

        Parameters:
        -----------
        top_k: int. Project the data onto this many top PCs.

        Returns:
        -----------
        ndarray. shape=(num_samps, num_selected_vars)

        TODO:
        - Project the data on the `top_k` PCs (assume PCA has already been performed).
        - Project this PCA-transformed data back to the original data space
        - If you normalized, remember to rescale the data projected back to the original data space.
        '''
        Ac = self.pca_project(np.arange(top_k)) #call the project function to project the data into PCA space
        sorig = self.orig_maxs - self.orig_mins
        if self.normalized == True:
            Ar = sorig * (Ac @ self.pMat.T + self.orig_means) + self.orig_mins #project the data back into the data space 
        else:
            Ar = Ac @ self.pMat.T + self.orig_means

        return Ar #return the data that has been projected back 



    def loading_plot(self):
        '''Create a loading plot of the top 2 PC eigenvectors

        (Week 2)

        TODO:
        - Plot a line joining the origin (0, 0) and corresponding components of the top 2 PC eigenvectors.
            Example: If e_0 = [0.1, 0.3] and e_1 = [1.0, 2.0], you would create two lines to join
            (0, 0) and (0.1, 1.0); (0, 0) and (0.3, 2.0).
            Number of lines = num_vars
        - Use plt.annotate to label each line by the variable that it corresponds to.
        - Reminder to create useful x and y axis labels.
        '''

        eigs = self.e_vecs[:, :2] #gets the first two eigenvectors from the eigenvectors.
        
        for i in range(len(self.e_vecs)):
            plt.plot([0, eigs[i, 0]], [0, eigs[i,1]]) #plots the line from the origin to the point of the eignevectors 
            plt.annotate(self.vars[i], (eigs[i, 0], eigs[i,1]), fontsize = 12) #adds a label for the variable it represents

        plt.xlabel("PC1") #labels
        plt.ylabel("PC2")
        plt.title("PC1 vs. PC2")

        

        

        
