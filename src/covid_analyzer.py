"""
COVID-19 Global Impact Analysis
Author: Data Analyst Portfolio
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

class COVIDAnalyzer:
    def __init__(self):
        """Initialize COVID-19 Analysis"""
        self.covid_data = None
        self.vaccination_data = None
        self.economic_data = None
        self.countries = None
        
    def load_data(self, generate_sample=True):
        """Load COVID-19 data from various sources"""
        if generate_sample:
            self.covid_data = self._generate_covid_data()
            self.vaccination_data = self._generate_vaccination_data()
            self.economic_data = self._generate_economic_data()
        else:
            # Load from actual data files
            self.covid_data = pd.read_csv('data/raw/covid_cases.csv')
            self.vaccination_data = pd.read_csv('data/raw/vaccinations.csv')
            self.economic_data = pd.read_csv('data/raw/economic_data.csv')
        
        print(f"Loaded COVID-19 data for {len(self.covid_data['country'].unique())} countries")
        return self.covid_data
    
    def _generate_covid_data(self):
        """Generate sample COVID-19 data"""
        np.random.seed(42)
        
        # Countries and regions
        countries = [
            'United States', 'India', 'Brazil', 'United Kingdom', 'France',
            'Germany', 'Italy', 'Spain', 'Russia', 'Turkey', 'Argentina',
            'Colombia', 'Mexico', 'Poland', 'Iran', 'Ukraine', 'South Africa',
            'Peru', 'Netherlands', 'Czech Republic', 'Indonesia', 'Belgium',
            'Iraq', 'Chile', 'Romania', 'Bangladesh', 'Philippines', 'Sweden',
            'Pakistan', 'Portugal', 'Israel', 'Hungary', 'Jordan', 'Serbia',
            'Switzerland', 'Japan', 'Austria', 'Lebanon', 'Morocco', 'UAE',
            'Saudi Arabia', 'Bulgaria', 'Slovakia', 'Croatia', 'Georgia',
            'Azerbaijan', 'Tunisia', 'Greece', 'Moldova', 'Belarus', 'Kuwait'
        ]
        
        # Generate data for 2 years (2020-2022)
        start_date = datetime(2020, 1, 1)
        end_date = datetime(2022, 12, 31)
        date_range = pd.date_range(start_date, end_date, freq='D')
        
        data = []
        for country in countries:
            # Country-specific parameters
            population = np.random.randint(1000000, 1500000000)
            base_cases = np.random.randint(10, 1000)
            growth_rate = np.random.uniform(0.05, 0.15)
            
            for date in date_range:
                # Simulate waves
                days_since_start = (date - start_date).days
                
                # Multiple waves
                wave1 = np.exp(-((days_since_start - 100) ** 2) / 2000)
                wave2 = np.exp(-((days_since_start - 400) ** 2) / 2000)
                wave3 = np.exp(-((days_since_start - 700) ** 2) / 2000)
                
                wave_factor = wave1 + 0.5 * wave2 + 0.3 * wave3
                
                # Daily cases with noise
                daily_cases = int(base_cases * wave_factor * (1 + np.random.normal(0, 0.3)))
                daily_cases = max(0, daily_cases)
                
                # Deaths (1-3% of cases)
                death_rate = np.random.uniform(0.01, 0.03)
                daily_deaths = int(daily_cases * death_rate * (1 + np.random.normal(0, 0.2)))
                daily_deaths = max(0, daily_deaths)
                
                data.append({
                    'date': date,
                    'country': country,
                    'daily_cases': daily_cases,
                    'daily_deaths': daily_deaths,
                    'total_cases': 0,  # Will be calculated
                    'total_deaths': 0   # Will be calculated
                })
        
        df = pd.DataFrame(data)
        
        # Calculate cumulative totals
        df = df.sort_values(['country', 'date'])
        df['total_cases'] = df.groupby('country')['daily_cases'].cumsum()
        df['total_deaths'] = df.groupby('country')['daily_deaths'].cumsum()
        
        return df
    
    def _generate_vaccination_data(self):
        """Generate sample vaccination data"""
        np.random.seed(42)
        
        countries = self.covid_data['country'].unique()
        start_date = datetime(2021, 1, 1)
        end_date = datetime(2022, 12, 31)
        date_range = pd.date_range(start_date, end_date, freq='D')
        
        data = []
        for country in countries:
            population = np.random.randint(1000000, 1500000000)
            max_vaccination_rate = np.random.uniform(0.6, 0.9)
            
            for date in date_range:
                days_since_start = (date - start_date).days
                
                # S-shaped vaccination curve
                vaccination_rate = max_vaccination_rate / (1 + np.exp(-(days_since_start - 200) / 50))
                vaccination_rate = min(vaccination_rate, max_vaccination_rate)
                
                daily_vaccinations = int(population * vaccination_rate * 0.001 * (1 + np.random.normal(0, 0.2)))
                daily_vaccinations = max(0, daily_vaccinations)
                
                data.append({
                    'date': date,
                    'country': country,
                    'daily_vaccinations': daily_vaccinations,
                    'total_vaccinations': 0,
                    'people_vaccinated': 0,
                    'people_fully_vaccinated': 0
                })
        
        df = pd.DataFrame(data)
        df = df.sort_values(['country', 'date'])
        df['total_vaccinations'] = df.groupby('country')['daily_vaccinations'].cumsum()
        df['people_vaccinated'] = df['total_vaccinations'] * 0.8
        df['people_fully_vaccinated'] = df['total_vaccinations'] * 0.6
        
        return df
    
    def _generate_economic_data(self):
        """Generate sample economic impact data"""
        np.random.seed(42)
        
        countries = self.covid_data['country'].unique()
        
        data = []
        for country in countries:
            # Pre-pandemic GDP
            gdp_2019 = np.random.uniform(10000000000, 20000000000000)
            
            # Economic impact factors
            impact_severity = np.random.uniform(0.02, 0.08)
            recovery_speed = np.random.uniform(0.5, 2.0)
            
            for year in [2019, 2020, 2021, 2022]:
                if year == 2019:
                    gdp = gdp_2019
                elif year == 2020:
                    # Sharp decline
                    gdp = gdp_2019 * (1 - impact_severity)
                else:
                    # Gradual recovery
                    recovery_factor = (year - 2020) * recovery_speed
                    gdp = gdp_2019 * (1 - impact_severity * np.exp(-recovery_factor))
                
                unemployment_rate = np.random.uniform(3, 15) if year >= 2020 else np.random.uniform(3, 8)
                
                data.append({
                    'country': country,
                    'year': year,
                    'gdp': gdp,
                    'gdp_growth': 0,  # Will be calculated
                    'unemployment_rate': unemployment_rate
                })
        
        df = pd.DataFrame(data)
        
        # Calculate GDP growth
        df = df.sort_values(['country', 'year'])
        df['gdp_growth'] = df.groupby('country')['gdp'].pct_change() * 100
        
        return df
    
    def analyze_global_trends(self):
        """Analyze global COVID-19 trends"""
        # Global daily totals
        global_daily = self.covid_data.groupby('date').agg({
            'daily_cases': 'sum',
            'daily_deaths': 'sum',
            'total_cases': 'sum',
            'total_deaths': 'sum'
        }).reset_index()
        
        # Calculate 7-day moving averages
        global_daily['cases_7day_avg'] = global_daily['daily_cases'].rolling(7).mean()
        global_daily['deaths_7day_avg'] = global_daily['daily_deaths'].rolling(7).mean()
        
        # Identify waves
        waves = self._identify_waves(global_daily)
        
        return global_daily, waves
    
    def _identify_waves(self, global_data):
        """Identify COVID-19 waves using peak detection"""
        from scipy.signal import find_peaks
        
        # Find peaks in daily cases
        cases_series = global_data['cases_7day_avg'].fillna(0)
        peaks, _ = find_peaks(cases_series, height=cases_series.max() * 0.3, distance=30)
        
        waves = []
        for i, peak_idx in enumerate(peaks):
            peak_date = global_data.iloc[peak_idx]['date']
            peak_cases = global_data.iloc[peak_idx]['cases_7day_avg']
            waves.append({
                'wave': i + 1,
                'peak_date': peak_date,
                'peak_cases': peak_cases
            })
        
        return waves
    
    def analyze_vaccination_effectiveness(self):
        """Analyze vaccination effectiveness"""
        # Merge COVID and vaccination data
        merged_data = pd.merge(
            self.covid_data, 
            self.vaccination_data, 
            on=['date', 'country'], 
            how='left'
        )
        
        # Calculate vaccination rates
        merged_data['vaccination_rate'] = merged_data['people_fully_vaccinated'] / merged_data['total_cases'].max()
        
        # Analyze correlation between vaccination and cases
        correlation_analysis = {}
        
        for country in merged_data['country'].unique():
            country_data = merged_data[merged_data['country'] == country]
            
            # Remove NaN values
            valid_data = country_data.dropna(subset=['vaccination_rate', 'daily_cases'])
            
            if len(valid_data) > 10:
                correlation = stats.pearsonr(valid_data['vaccination_rate'], valid_data['daily_cases'])
                correlation_analysis[country] = {
                    'correlation': correlation[0],
                    'p_value': correlation[1],
                    'data_points': len(valid_data)
                }
        
        return correlation_analysis
    
    def analyze_economic_impact(self):
        """Analyze economic impact of COVID-19"""
        # Calculate economic impact metrics
        economic_impact = {}
        
        for country in self.economic_data['country'].unique():
            country_data = self.economic_data[self.economic_data['country'] == country]
            
            # Pre-pandemic vs pandemic GDP
            gdp_2019 = country_data[country_data['year'] == 2019]['gdp'].iloc[0]
            gdp_2020 = country_data[country_data['year'] == 2020]['gdp'].iloc[0]
            gdp_2022 = country_data[country_data['year'] == 2022]['gdp'].iloc[0]
            
            # Impact metrics
            initial_impact = (gdp_2020 - gdp_2019) / gdp_2019 * 100
            recovery_rate = (gdp_2022 - gdp_2020) / gdp_2020 * 100
            
            economic_impact[country] = {
                'initial_impact_pct': initial_impact,
                'recovery_rate_pct': recovery_rate,
                'gdp_2019': gdp_2019,
                'gdp_2020': gdp_2020,
                'gdp_2022': gdp_2022
            }
        
        return economic_impact
    
    def create_visualizations(self, save_plots=True):
        """Create comprehensive visualizations"""
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        
        # 1. Global Trends
        global_daily, waves = self.analyze_global_trends()
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Global cases over time
        axes[0, 0].plot(global_daily['date'], global_daily['cases_7day_avg'], linewidth=2)
        axes[0, 0].set_title('Global Daily Cases (7-day average)')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel('Daily Cases')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Global deaths over time
        axes[0, 1].plot(global_daily['date'], global_daily['deaths_7day_avg'], linewidth=2, color='red')
        axes[0, 1].set_title('Global Daily Deaths (7-day average)')
        axes[0, 1].set_xlabel('Date')
        axes[0, 1].set_ylabel('Daily Deaths')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Top 10 countries by total cases
        top_countries = self.covid_data.groupby('country')['total_cases'].max().sort_values(ascending=False).head(10)
        axes[1, 0].barh(range(len(top_countries)), top_countries.values)
        axes[1, 0].set_yticks(range(len(top_countries)))
        axes[1, 0].set_yticklabels(top_countries.index)
        axes[1, 0].set_title('Top 10 Countries by Total Cases')
        axes[1, 0].set_xlabel('Total Cases')
        
        # Economic impact
        economic_impact = self.analyze_economic_impact()
        impact_data = pd.DataFrame(economic_impact).T
        axes[1, 1].scatter(impact_data['initial_impact_pct'], impact_data['recovery_rate_pct'], alpha=0.6)
        axes[1, 1].set_xlabel('Initial Economic Impact (%)')
        axes[1, 1].set_ylabel('Recovery Rate (%)')
        axes[1, 1].set_title('Economic Impact vs Recovery Rate')
        
        plt.tight_layout()
        
        if save_plots:
            plt.savefig('results/covid_global_analysis.png', dpi=300, bbox_inches='tight')
        
        plt.show()
        
        # 2. Interactive Plotly visualizations
        self._create_interactive_plots()
    
    def _create_interactive_plots(self):
        """Create interactive Plotly visualizations"""
        global_daily, waves = self.analyze_global_trends()
        
        # Global trends with waves marked
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=global_daily['date'],
            y=global_daily['cases_7day_avg'],
            mode='lines',
            name='Daily Cases (7-day avg)',
            line=dict(color='blue', width=2)
        ))
        
        # Mark wave peaks
        for wave in waves:
            fig.add_trace(go.Scatter(
                x=[wave['peak_date']],
                y=[wave['peak_cases']],
                mode='markers',
                name=f"Wave {wave['wave']} Peak",
                marker=dict(size=10, color='red')
            ))
        
        fig.update_layout(
            title='Global COVID-19 Cases with Wave Peaks',
            xaxis_title='Date',
            yaxis_title='Daily Cases (7-day average)',
            hovermode='x unified'
        )
        
        fig.show()
        
        # Vaccination effectiveness
        vaccination_analysis = self.analyze_vaccination_effectiveness()
        effectiveness_df = pd.DataFrame(vaccination_analysis).T
        
        fig2 = px.scatter(
            effectiveness_df,
            x='correlation',
            y='p_value',
            title='Vaccination Effectiveness by Country',
            labels={'correlation': 'Correlation with Cases', 'p_value': 'P-value'},
            hover_data=['data_points']
        )
        
        fig2.show()
    
    def generate_insights_report(self):
        """Generate comprehensive insights report"""
        global_daily, waves = self.analyze_global_trends()
        vaccination_analysis = self.analyze_vaccination_effectiveness()
        economic_impact = self.analyze_economic_impact()
        
        report = {
            'summary': {
                'total_countries': len(self.covid_data['country'].unique()),
                'date_range': f"{self.covid_data['date'].min()} to {self.covid_data['date'].max()}",
                'total_cases': self.covid_data['total_cases'].max(),
                'total_deaths': self.covid_data['total_deaths'].max(),
                'number_of_waves': len(waves)
            },
            'waves': waves,
            'vaccination_effectiveness': {
                'countries_analyzed': len(vaccination_analysis),
                'average_correlation': np.mean([v['correlation'] for v in vaccination_analysis.values()]),
                'significant_correlations': len([v for v in vaccination_analysis.values() if v['p_value'] < 0.05])
            },
            'economic_impact': {
                'average_initial_impact': np.mean([v['initial_impact_pct'] for v in economic_impact.values()]),
                'average_recovery_rate': np.mean([v['recovery_rate_pct'] for v in economic_impact.values()]),
                'most_affected_countries': sorted(economic_impact.items(), key=lambda x: x[1]['initial_impact_pct'])[:5]
            }
        }
        
        return report
    
    def save_results(self, output_dir='results'):
        """Save analysis results"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Save processed data
        global_daily, waves = self.analyze_global_trends()
        global_daily.to_csv(f'{output_dir}/global_trends.csv', index=False)
        
        # Save vaccination analysis
        vaccination_analysis = self.analyze_vaccination_effectiveness()
        pd.DataFrame(vaccination_analysis).T.to_csv(f'{output_dir}/vaccination_effectiveness.csv')
        
        # Save economic analysis
        economic_impact = self.analyze_economic_impact()
        pd.DataFrame(economic_impact).T.to_csv(f'{output_dir}/economic_analysis.csv')
        
        # Save insights report
        insights = self.generate_insights_report()
        import json
        with open(f'{output_dir}/insights_report.json', 'w') as f:
            json.dump(insights, f, indent=2, default=str)
        
        print(f"Results saved to {output_dir}/ directory")

def main():
    """Main function to run COVID-19 analysis"""
    print("🦠 Starting COVID-19 Global Impact Analysis")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = COVIDAnalyzer()
    
    # Load data
    print("Loading COVID-19 data...")
    covid_data = analyzer.load_data()
    
    # Analyze global trends
    print("Analyzing global trends...")
    global_daily, waves = analyzer.analyze_global_trends()
    print(f"Identified {len(waves)} COVID-19 waves")
    
    # Analyze vaccination effectiveness
    print("💉 Analyzing vaccination effectiveness...")
    vaccination_analysis = analyzer.analyze_vaccination_effectiveness()
    print(f"Analyzed vaccination data for {len(vaccination_analysis)} countries")
    
    # Analyze economic impact
    print("Analyzing economic impact...")
    economic_impact = analyzer.analyze_economic_impact()
    print(f"Analyzed economic data for {len(economic_impact)} countries")
    
    # Generate insights
    print("Generating insights...")
    insights = analyzer.generate_insights_report()
    print(f"\nKey Insights:")
    print(f"- Total cases: {insights['summary']['total_cases']:,}")
    print(f"- Total deaths: {insights['summary']['total_deaths']:,}")
    print(f"- Countries analyzed: {insights['summary']['total_countries']}")
    print(f"- Average economic impact: {insights['economic_impact']['average_initial_impact']:.1f}%")
    
    # Create visualizations
    print("\nCreating visualizations...")
    analyzer.create_visualizations()
    
    # Save results
    print("\nSaving results...")
    analyzer.save_results()
    
    print("\nCOVID-19 analysis complete! Check the results/ directory for output files.")

if __name__ == "__main__":
    main()
