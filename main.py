
import abc


class ValidationResult:
    def __init__(self, result: bool, result_details: str):
        self.result = result
        self.result_details = result_details


class ValidationAdapter:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def validate(self, data: str) -> ValidationResult:
        """validate all the stuff"""
        pass


class OutputAdapter:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle(self, data: ValidationResult):
        """Present output"""
        pass


class S3ValidationAdapter(ValidationAdapter):

    def validate(self, query) -> ValidationResult:
        print('do S3 Validation')
        validation_result = ValidationResult(True, "passed S3 validation")
        return validation_result


class DatabricksValidationAdapter(ValidationAdapter):

    def validate(self, data) -> ValidationResult:
        print('do Databricks Validation')
        validation_result = ValidationResult(True, "passed Databricks validation")
        return validation_result


class S3OutputAdapter(OutputAdapter):

    def handle(self, data: ValidationResult):
        print(f"validation S3  output result: {data.result}")
        print(f"validation S3  output result details: {data.result_details}")


class SomeOtherOutputAdapter(OutputAdapter):

    def handle(self, data: ValidationResult):
        print(f"validation some other output result: {data.result}")
        print(f"validation some other output result details: {data.result_details}")


class DomainValidatorService:
    def __init__(self, validation_adapter: ValidationAdapter, output_adapter: OutputAdapter):
        self.validation_adapter = validation_adapter
        self.output_adapter = output_adapter

    def run_validation(self, data) :
        return self.output_adapter.handle(self.validation_adapter.validate(data))


if __name__ == '__main__':
    validation_type_registry = {
        'S3': S3ValidationAdapter,
        'Databricks': DatabricksValidationAdapter
    }

    output_type_registry = {
        'S3': S3OutputAdapter,
        'someother': SomeOtherOutputAdapter
    }

    """validation type would be passed in as argument in request"""
    validation_type_requested = "S3"

    validation_adapter = validation_type_registry[validation_type_requested]()
    output_adapter = output_type_registry[validation_type_requested]()

    domainValidator = DomainValidatorService(validation_adapter=validation_adapter, output_adapter=output_adapter)
    domainValidator.run_validation("some data to validate")




