package com.example.service;

import com.example.repository.EntityRepository;
import com.example.model.Entity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

/**
 * Service for [ENTITY_NAME] business logic.
 *
 * Follows best practices:
 * - Single Responsibility Principle (only handles [ENTITY_NAME] business logic)
 * - Dependency Inversion (depends on repository interface)
 * - Uses Optional instead of null
 * - Transaction management with @Transactional
 */
@Service
public class EntityService {

    private final EntityRepository entityRepository;

    /**
     * Constructor injection (recommended for required dependencies).
     */
    public EntityService(EntityRepository entityRepository) {
        this.entityRepository = entityRepository;
    }

    /**
     * Finds entity by ID.
     *
     * @param id the entity ID
     * @return Optional containing the entity if found
     */
    public Optional<Entity> findById(Long id) {
        return entityRepository.findById(id);
    }

    /**
     * Finds all entities.
     *
     * @return list of all entities (never null, may be empty)
     */
    public List<Entity> findAll() {
        return entityRepository.findAll();
    }

    /**
     * Creates a new entity.
     *
     * @param entity the entity to create (must not be null)
     * @return the created entity with generated ID
     * @throws IllegalArgumentException if entity is null
     */
    @Transactional
    public Entity create(Entity entity) {
        if (entity == null) {
            throw new IllegalArgumentException("Entity cannot be null");
        }

        validate(entity);
        return entityRepository.save(entity);
    }

    /**
     * Updates an existing entity.
     *
     * @param id the entity ID
     * @param entity the updated entity data
     * @return Optional containing the updated entity if found
     */
    @Transactional
    public Optional<Entity> update(Long id, Entity entity) {
        return entityRepository.findById(id)
            .map(existingEntity -> {
                updateFields(existingEntity, entity);
                validate(existingEntity);
                return entityRepository.save(existingEntity);
            });
    }

    /**
     * Deletes an entity by ID.
     *
     * @param id the entity ID
     * @return true if entity was deleted, false if not found
     */
    @Transactional
    public boolean delete(Long id) {
        return entityRepository.findById(id)
            .map(entity -> {
                entityRepository.delete(entity);
                return true;
            })
            .orElse(false);
    }

    /**
     * Validates entity business rules.
     *
     * @param entity the entity to validate
     * @throws ValidationException if validation fails
     */
    private void validate(Entity entity) {
        // Add validation logic
        // Example: if (entity.getName() == null || entity.getName().trim().isEmpty()) {
        //     throw new ValidationException("Name is required");
        // }
    }

    /**
     * Updates fields from source to target entity.
     *
     * @param target the entity to update
     * @param source the entity with new data
     */
    private void updateFields(Entity target, Entity source) {
        // Update only allowed fields
        // Example: target.setName(source.getName());
    }
}
