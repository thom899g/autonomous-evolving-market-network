"""
Configuration for Autonomous Evolving Market Network
Centralizes all configurable parameters with validation
"""

import os
from typing import Dict, Any
from dataclasses import dataclass, field
from enum import Enum

class AgentType(Enum):
    """Types of trading agents in the ecosystem"""
    MARKET_MAKER = "market_maker"
    ARBITRAGEUR = "arbitrageur"
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    EVOLVING = "evolving"

class MarketMode(Enum):
    """Market operation modes"""
    SIMULATION = "simulation"
    PAPER_TRADING = "paper_trading"
    LIVE = "live"

@dataclass
class AgentConfig:
    """Configuration for individual agents"""
    agent_id: str
    agent_type: AgentType
    initial_capital: float = 10000.0
    risk_tolerance: float = 0.02  # 2% max risk per trade
    learning_rate: float = 0.001
    exploration_rate: float = 0.1
    memory_size: int = 1000
    update_frequency: int = 60  # seconds
    
    def validate(self) -> bool:
        """Validate configuration parameters"""
        if self.risk_tolerance <= 0 or self.risk_tolerance > 0.5:
            raise ValueError(f"Risk tolerance {self.risk_tolerance} must be between 0 and 0.5")
        if self.initial_capital <= 0:
            raise ValueError("Initial capital must be positive")
        return True

@dataclass
class FirebaseConfig:
    """Firebase configuration with validation"""
    project_id: str = field(default_factory=lambda: os.getenv("FIREBASE_PROJECT_ID", ""))
    credentials_path: str = field(default_factory=lambda: os.getenv("GOOGLE_APPLICATION_CREDENTIALS", ""))
    
    # Collections
    AGENTS_COLLECTION: str = "market_agents"
    TRANSACTIONS_COLLECTION: str = "transactions"
    MARKET_DATA_COLLECTION: str = "market_data"
    COORDINATION_COLLECTION: str = "coordination"
    
    def validate(self) -> bool:
        """Validate Firebase configuration"""
        if not self.project_id:
            raise ValueError("FIREBASE_PROJECT_ID environment variable not set")
        if not os.path.exists(self.credentials_path):
            raise FileNotFoundError(f"Firebase credentials not found at {self.credentials_path}")
        return True

@dataclass
class MarketConfig:
    """Market simulation and trading configuration"""
    mode: MarketMode = MarketMode.SIMULATION
    symbols: list = field(default_factory=lambda: ["BTC/USDT", "ETH/USDT", "SOL/USDT"])
    data_source: str = "simulation"  # 'ccxt', 'simulation', 'database'
    simulation_speed: int = 1  # 1x real time
    fee_structure: Dict[str, float] = field(default_factory=lambda: {"maker": 0.001, "taker": 0.002})
    
    def validate(self) -> bool:
        """Validate market configuration"""
        if not self.symbols:
            raise ValueError("At least one trading symbol must be specified")
        if self.simulation_speed <= 0:
            raise ValueError("Simulation speed must be positive")
        return True

@dataclass 
class EvolutionConfig:
    """Evolutionary algorithm configuration"""
    population_size: int = 10
    mutation_rate: float = 0.05
    crossover_rate: float = 0.7
    elitism_count: int = 2
    fitness_window: int = 100  # trades to evaluate fitness
    selection_pressure: float = 2.0
    
    def validate(self) -> bool:
        """Validate evolution parameters"""
        if self.population_size < 2:
            raise ValueError("Population size must be at least 2")
        if not 0 <= self.mutation_rate <= 1:
            raise ValueError("Mutation rate must be between 0 and 1")
        return True

class GlobalConfig:
    """Singleton configuration manager"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize configuration with environment variables"""
        self.agent = AgentConfig(
            agent_id=os.getenv("AGENT_ID", f"agent_{os.urandom(4).hex()}"),
            agent_type=AgentType(os.getenv("AGENT_TYPE", "evolving"))
        )
        
        self.firebase = FirebaseConfig()
        self.market = MarketConfig(
            mode=MarketMode(os.getenv("MARKET_MODE", "simulation"))
        )
        self.evolution = EvolutionConfig()
        
        # Validate all configurations
        self.validate_all()
    
    def validate_all(self):
        """Validate all configuration sections"""
        self.agent.validate()
        self.firebase.validate()
        self.market.validate()
        self.evolution.validate()
        return True

# Export global configuration instance
config = GlobalConfig()