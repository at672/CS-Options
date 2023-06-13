import numpy as np
from scipy.stats import norm

def BMS_d1(S, K, r, q, sigma, tau):
    ''' Computes d1 for the Black Merton Scholes formula '''
    d1 = 1.0*(np.log(1.0 * S/K) + (r - q + sigma**2/2) * tau) / (sigma * np.sqrt(tau))
    return d1

def BMS_d2(S, K, r, q, sigma, tau):
    ''' Computes d2 for the Black Merton Scholes formula '''
    d2 = 1.0*(np.log(1.0 * S/K) + (r - q - sigma**2/2) * tau) / (sigma * np.sqrt(tau))
    return d2

def BMS_price(type_option, S, K, r, q, sigma, T, t=0):
    ''' Computes the Black Merton Scholes price for a 'call' or 'put' option '''
    tau = T - t
    d1 = BMS_d1(S, K, r, q, sigma, tau)
    d2 = BMS_d2(S, K, r, q, sigma, tau)
    if type_option == 'call':
        price = S * np.exp(-q * tau) * norm.cdf(d1) - K * np.exp(-r * tau) * norm.cdf(d2)
    elif type_option == 'put':
        price = K * np.exp(-r * tau) * norm.cdf(-d2) - S * np.exp(-q * tau) * norm.cdf(-d1) 
    return price

def BMS_delta(type_option, S, K, r, q, sigma, T, t=0):
    ''' Computes the delta for a call or a put. '''
    tau = T - t
    d1 = BMS_d1(S, K, r, q, sigma, tau)
    if type_option == 'call':
        delta = np.exp(-q * tau) * norm.cdf(d1)
    elif type_option == 'put':
        delta = np.exp(-q * tau) * (norm.cdf(d1) - 1)
    return delta

def BMS_gamma(type_option, S, K, r, q, sigma, T, t=0):
	tau = T-t
	d1 = BMS_d1(S, K, r, q, sigma, tau)
	gamma = np.exp(-q*tau)*norm.pdf(d1)/(S*sigma*np.sqrt(tau))
	#gamma put = gamma call
	return gamma

def BMS_vega(type_option, S, K, r, q, sigma, T, t=0):
	tau = T-t
	d1 = BMS_d1(S, K, r, q, sigma, tau)
	vega = S*np.sqrt(tau)*np.exp(-q*tau)*norm.pdf(d1)
	#vega put = vega call
	return vega

def BMS_theta( type_option, S, K, r, q, sigma, T, t=0):
	tau = T-t
	d1 = BMS_d1(S, K, r, q, sigma, tau)
	d2 = BMS_d2(S, K, r, q, sigma, tau)
	if type_option == 'call':
		theta = -(S*np.exp(-q*tau)*norm.pdf(d1)*sigma)/(2*np.sqrt(tau)) - r*K*np.exp(-r*tau)*norm.cdf(d2) + q*S*np.exp(-q*tau)*norm.cdf(d1)
	elif type_option == 'put':
		theta = -(S*np.exp(-q*tau)*norm.pdf(d1)*sigma)/(2*np.sqrt(tau)) + r*K*np.exp(-r*tau)*norm.cdf(-d2) - q*S*np.exp(-q*tau)*norm.cdf(-d1)
	return theta

#PNL Approx
#Delta * dS + Gamma * 0.5 * dS**2 + Vega * dsigma + Theta * dt