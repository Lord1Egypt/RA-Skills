package com.example.service;

import com.example.model.Entity;
import com.example.repository.EntityRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.Mockito.*;

/**
 * Unit tests for EntityService.
 *
 * Follows best practices:
 * - AAA pattern (Arrange-Act-Assert)
 * - Descriptive test names
 * - Proper use of mocks
 * - Tests one behavior per test method
 * - Uses @Nested for logical grouping
 * - Uses @ParameterizedTest for multiple inputs
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("Entity Service Tests")
class EntityServiceTest {

    @Mock
    private EntityRepository entityRepository;

    @InjectMocks
    private EntityService entityService;

    private Entity testEntity;

    @BeforeEach
    void setUp() {
        // Arrange - Common test data
        testEntity = new Entity();
        testEntity.setId(1L);
        testEntity.setName("Test Entity");
    }

    @Nested
    @DisplayName("Find Operations")
    class FindOperations {

        @Test
        @DisplayName("Should find entity by ID when entity exists")
        void shouldFindEntityByIdWhenExists() {
            // Arrange
            when(entityRepository.findById(1L)).thenReturn(Optional.of(testEntity));

            // Act
            Optional<Entity> result = entityService.findById(1L);

            // Assert
            assertTrue(result.isPresent());
            assertEquals(testEntity, result.get());
            verify(entityRepository).findById(1L);
        }

        @Test
        @DisplayName("Should return empty Optional when entity not found")
        void shouldReturnEmptyWhenEntityNotFound() {
            // Arrange
            when(entityRepository.findById(anyLong())).thenReturn(Optional.empty());

            // Act
            Optional<Entity> result = entityService.findById(999L);

            // Assert
            assertFalse(result.isPresent());
            verify(entityRepository).findById(999L);
        }

        @Test
        @DisplayName("Should find all entities")
        void shouldFindAllEntities() {
            // Arrange
            List<Entity> entities = Arrays.asList(testEntity, new Entity());
            when(entityRepository.findAll()).thenReturn(entities);

            // Act
            List<Entity> result = entityService.findAll();

            // Assert
            assertNotNull(result);
            assertEquals(2, result.size());
            verify(entityRepository).findAll();
        }
    }

    @Nested
    @DisplayName("Create Operations")
    class CreateOperations {

        @Test
        @DisplayName("Should create entity with valid data")
        void shouldCreateEntityWithValidData() {
            // Arrange
            Entity newEntity = new Entity();
            newEntity.setName("New Entity");

            when(entityRepository.save(any(Entity.class))).thenReturn(testEntity);

            // Act
            Entity result = entityService.create(newEntity);

            // Assert
            assertNotNull(result);
            assertEquals(testEntity.getId(), result.getId());
            verify(entityRepository).save(newEntity);
        }

        @Test
        @DisplayName("Should throw exception when creating null entity")
        void shouldThrowExceptionWhenCreatingNull() {
            // Act & Assert
            assertThrows(IllegalArgumentException.class, () ->
                entityService.create(null));

            verify(entityRepository, never()).save(any());
        }

        @ParameterizedTest
        @ValueSource(strings = {"", "  ", "\t", "\n"})
        @DisplayName("Should throw exception for invalid names")
        void shouldThrowExceptionForInvalidNames(String invalidName) {
            // Arrange
            Entity entity = new Entity();
            entity.setName(invalidName);

            // Act & Assert
            assertThrows(ValidationException.class, () ->
                entityService.create(entity));

            verify(entityRepository, never()).save(any());
        }
    }

    @Nested
    @DisplayName("Update Operations")
    class UpdateOperations {

        @Test
        @DisplayName("Should update entity when it exists")
        void shouldUpdateEntityWhenExists() {
            // Arrange
            Entity updatedEntity = new Entity();
            updatedEntity.setName("Updated Name");

            when(entityRepository.findById(1L)).thenReturn(Optional.of(testEntity));
            when(entityRepository.save(any(Entity.class))).thenReturn(testEntity);

            // Act
            Optional<Entity> result = entityService.update(1L, updatedEntity);

            // Assert
            assertTrue(result.isPresent());
            verify(entityRepository).findById(1L);
            verify(entityRepository).save(testEntity);
        }

        @Test
        @DisplayName("Should return empty Optional when updating non-existent entity")
        void shouldReturnEmptyWhenUpdatingNonExistent() {
            // Arrange
            when(entityRepository.findById(anyLong())).thenReturn(Optional.empty());

            // Act
            Optional<Entity> result = entityService.update(999L, new Entity());

            // Assert
            assertFalse(result.isPresent());
            verify(entityRepository, never()).save(any());
        }
    }

    @Nested
    @DisplayName("Delete Operations")
    class DeleteOperations {

        @Test
        @DisplayName("Should delete entity when it exists")
        void shouldDeleteEntityWhenExists() {
            // Arrange
            when(entityRepository.findById(1L)).thenReturn(Optional.of(testEntity));

            // Act
            boolean result = entityService.delete(1L);

            // Assert
            assertTrue(result);
            verify(entityRepository).findById(1L);
            verify(entityRepository).delete(testEntity);
        }

        @Test
        @DisplayName("Should return false when deleting non-existent entity")
        void shouldReturnFalseWhenDeletingNonExistent() {
            // Arrange
            when(entityRepository.findById(anyLong())).thenReturn(Optional.empty());

            // Act
            boolean result = entityService.delete(999L);

            // Assert
            assertFalse(result);
            verify(entityRepository).findById(999L);
            verify(entityRepository, never()).delete(any());
        }
    }

    @Nested
    @DisplayName("Validation Tests")
    class ValidationTests {

        @ParameterizedTest
        @CsvSource({
            "Valid Name, true",
            "'', false",
            "'  ', false",
            "null, false"
        })
        @DisplayName("Should validate entity names correctly")
        void shouldValidateEntityNames(String name, boolean shouldPass) {
            // Arrange
            Entity entity = new Entity();
            if (!"null".equals(name)) {
                entity.setName(name);
            }

            // Act & Assert
            if (shouldPass) {
                assertDoesNotThrow(() -> entityService.create(entity));
            } else {
                assertThrows(ValidationException.class, () ->
                    entityService.create(entity));
            }
        }
    }
}
